from fastapi import APIRouter, Depends

from app.api_requests.user_request import UserRequest
from app.database.session import DatabaseSessionManager
from app.response.generic_response import GenericResponse
from app.services.admin_service import AdminService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/admin',
    tags=['Create/Update Business Users (Only For Admins)']
)

db_manager = DatabaseSessionManager()


@router.post("/create/user")
def create_user(request: UserRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_user(request=request)


@router.post("/update/user/{user_id}")
def update_user(user_id: int, request: UserRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_user(user_id=user_id, request=request)
