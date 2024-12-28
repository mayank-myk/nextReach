import time
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteException
from uvicorn.workers import UvicornWorker

from app.exceptions import GenericException
from app.exceptions.error_response import ErrorResponse
from app.exceptions.validation_exceptions import MissingRequiredField
from app.routers import admin_resource, campaign_resource, website_resource, user_resource, influencer_resource
from app.utils.logger import configure_logger

load_dotenv()

log = configure_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up the application...")
    try:
        yield
    finally:
        log.info("Shutting down the application...")


server = FastAPI(title="Scalable FastAPI Project", lifespan=lifespan)

server.include_router(admin_resource.router)
server.include_router(campaign_resource.router)
server.include_router(user_resource.router)
server.include_router(website_resource.router)
server.include_router(influencer_resource.router)


class AsyncioUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "asyncio", "http": "auto"}


@server.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time_ms = "{:.3f}".format((time.time() - start_time) * 1000)
    log.info(
        event="Processed Request",
        path=request.url.path,
        duration_ms=process_time_ms,
        query_params=request.query_params,
        path_params=request.path_params,
    )
    response.headers["x-response-time-ms"] = process_time_ms
    return response


@server.exception_handler(StarletteException)
async def http_exception_handler(request: Request, ex: StarletteException):
    params = {"q": request.query_params.__str__(), "path": request.url.__str__()}
    log.error(event="Api failed", status_code=ex.status_code, detail=ex.detail, params=params)
    context = ErrorResponse.builder(ex)
    return ORJSONResponse(status_code=ex.status_code, content=context)


@server.exception_handler(GenericException)
async def generic_exception_handler(request: Request, ex: GenericException):
    params = {"q": request.query_params.__str__(), "path": request.url.__str__()}
    log.error(event="Generic Exception", status_code=ex.status_code, params=params)
    return ORJSONResponse(status_code=ex.status_code, content=ErrorResponse.builder(ex))


@server.exception_handler(Exception)
async def exception_handler(request: Request, ex: Exception):
    params = {"q": request.query_params.__str__(), "path": request.url.__str__()}
    log.error(event="Unknown Exception", status_code=500, params=params)
    json_response = ErrorResponse.builder(ex)
    return ORJSONResponse(status_code=500, content=json_response)


@server.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, ex: RuntimeError):
    params = {"q": request.query_params.__str__(), "path": request.url.__str__()}
    log.error(event="Runtime Exception", status_code=500, params=params)
    json_response = ErrorResponse.builder(ex)
    return ORJSONResponse(status_code=500, content=json_response)


@server.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    params = {"q": request.query_params.__str__(), "path": request.url.__str__()}
    log.error(event="Validation Exception", params=params)
    # Returning the first validation error.
    raise MissingRequiredField(
        field=".".join([str(each) for each in details[0]["loc"]])
    )


if __name__ == "__main__":
    load_dotenv(dotenv_path='/Users/mayank.agrawal/PycharmProjects/nextReach/.env')
    uvicorn.run(server, host="0.0.0.0", port=8000)
