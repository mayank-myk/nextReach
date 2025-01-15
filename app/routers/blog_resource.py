from fastapi import APIRouter, Depends

from app.api_requests.blog_request import BlogRequest
from app.database.session import DatabaseSessionManager
from app.response.generic_response import GenericResponse
from app.services.admin_service import AdminService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/web',
    tags=['Blog Resources (Only For Website)']
)

db_manager = DatabaseSessionManager()


@router.post("/create/blog")
def create_blog(request: BlogRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_lead(request=request)


@router.post("/update/blog")
def update_blog(request: BlogRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_lead(request=request)
