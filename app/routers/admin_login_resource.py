from fastapi import APIRouter, Depends

from app.api_requests.admin_user_request import AdminUserRequest
from app.api_requests.login_request import LoginRequest
from app.database.session import DatabaseSessionManager
from app.response.generic_response import GenericResponse
from app.response.login_response import LoginResponse
from app.services.admin_service import AdminService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/admin',
    tags=['Admin login resource (Only For Website)']
)

db_manager = DatabaseSessionManager()


@router.post("/login")
def admin_login(request: LoginRequest, db=Depends(db_manager.get_db)) -> LoginResponse:
    admin_service = AdminService(db)
    return admin_service.admin_login(request=request)


@router.post("/create")
def create_admin(user: AdminUserRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_admin(new_user=user)


@router.post("/update")
def update_admin(user: AdminUserRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_admin(user=user)


@router.put("/delete")
def delete_admin(admin_id: str, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.delete_admin(admin_id=admin_id)
