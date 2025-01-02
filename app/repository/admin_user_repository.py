from typing import Optional

from sqlalchemy.orm import Session

from app.database.admin_user_table import AdminUser
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.api_requests.admin_user_request import AdminUserRequest
from app.utils.logger import configure_logger

_log = configure_logger()


class AdminUserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_admin(self, request: AdminUserRequest) -> AdminUser:
        try:
            new_admin = AdminUser(
                created_by=request.created_by,
                admin_id=request.admin_id,
                password=request.password,
                admin_type=request.admin_type
            )

            self.db.add(new_admin)
            self.db.commit()
            self.db.refresh(new_admin)
            return new_admin
        except Exception as ex:
            _log.error(f"Unable to create admin record with admin_id {request.admin_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, request.admin_id)

    def update_admin(self, request: AdminUserRequest) -> Optional[AdminUser]:
        try:
            existing_admin = self.db.query(AdminUser).filter(AdminUser.admin_id == request.admin_id).first()

            if not existing_admin:
                return None

            setattr(existing_admin, 'password', request.password)
            setattr(existing_admin, 'admin_type', request.admin_type)

            self.db.commit()
            self.db.refresh(existing_admin)
            return existing_admin
        except Exception as ex:
            _log.error(f"Unable to update admin record with admin_id {request.admin_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, request.admin_id)

    def delete_admin(self, admin_id: str) -> Optional[AdminUser]:
        try:
            existing_admin = self.db.query(AdminUser).filter(AdminUser.admin_id == admin_id).first()

            if not existing_admin:
                return None

            self.db.delete(existing_admin)
            self.db.commit()
            return existing_admin
        except Exception as ex:
            _log.error(f"Unable to delete admin record with admin_id {admin_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, admin_id)

    def get_admin_by_admin_id(self, admin_id: str) -> Optional[AdminUser]:

        try:
            existing_admin = self.db.query(AdminUser).filter(AdminUser.admin_id == admin_id).first()
            if not existing_admin:
                return None
            return existing_admin

        except Exception as ex:
            _log.error(f"Unable to fetch admin record with admin_id {admin_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, admin_id)
