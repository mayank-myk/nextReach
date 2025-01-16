from fastapi import APIRouter, Depends

from app.api_requests.blog_request import BlogRequest
from app.api_requests.next_reach_academy_request import NextReachAcademyRequest
from app.api_requests.success_story_request import SuccessStoryRequest
from app.database.session import DatabaseSessionManager
from app.response.generic_response import GenericResponse
from app.services.admin_service import AdminService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/admin',
    tags=['Blog, Success Stories, Academy (Only For Admins)']
)

db_manager = DatabaseSessionManager()


@router.post("/create/blog")
def create_blog(request: BlogRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_blog(request=request)


@router.post("/update/blog/{blog_id}")
def update_blog(blog_id: int, request: BlogRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_blog(blog_id=blog_id, request=request)


@router.post("/create/success-story")
def create_ss(request: SuccessStoryRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_ss(request=request)


@router.post("/update/success-story/{ss_id}")
def update_ss(ss_id: int, request: SuccessStoryRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_ss(ss_id=ss_id, request=request)


@router.post("/create/academy-video")
def create_nra(request: NextReachAcademyRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_nra(request=request)


@router.post("/update/academy-video/{nra_id}")
def update_nra(nra_id: int, request: NextReachAcademyRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_nra(nra_id=nra_id, request=request)
