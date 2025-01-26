import time
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteException
from uvicorn.workers import UvicornWorker

from app.exceptions import GenericException
from app.exceptions.error_response import ErrorResponse
from app.exceptions.validation_exceptions import MissingRequiredField
from app.routers import admin_resource, campaign_resource, website_resource, influencer_resource, lead_resource, \
    client_resource, website_client_resource, influencer_metric_resource, blog_resource, admin_login_resource
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


server = FastAPI(title="NextReach Admin Console", lifespan=lifespan, docs_url=None, redoc_url=None)

server.include_router(admin_resource.router)
server.include_router(admin_login_resource.router)
server.include_router(blog_resource.router)
server.include_router(campaign_resource.router)
server.include_router(lead_resource.router)
server.include_router(client_resource.router)
server.include_router(influencer_metric_resource.router)
server.include_router(influencer_resource.router)
server.include_router(website_client_resource.router)
server.include_router(website_resource.router)


@server.get("/february", include_in_schema=False)
async def custom_swagger_ui():
    """
    Custom Swagger UI route.
    """
    return get_swagger_ui_html(
        openapi_url="/february/openapi.json",
        title="My API Documentation"
    )


@server.get("/february/doc", include_in_schema=False)
async def custom_redoc_ui():
    """
    Custom ReDoc route.
    """
    return get_redoc_html(
        openapi_url="/february/openapi.json",  # Use your custom OpenAPI route
        title="Custom API Documentation"
    )


# Custom OpenAPI JSON route
@server.get("/february/openapi.json", include_in_schema=False)
async def custom_openapi():
    """
    Custom OpenAPI JSON route.
    """
    return get_openapi(
        title=server.title,
        version=server.version,
        description=server.description,
        routes=server.routes
    )


@server.get("/")
async def read_root():
    return {"message": "Do not try again, I dare you"}


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
    uvicorn.run(server, host="0.0.0.0", port=8010)
