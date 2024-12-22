from sqlalchemy.orm import Session

from app.database.admin_user_table import AdminUser
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.requests.admin_user_request import AdminUserRequest
from app.utils.logger import configure_logger

_log = configure_logger()


class AdminUserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_admin(self, request: AdminUserRequest) -> AdminUser:
        try:
            new_admin = AdminUser(
                created_by=request.created_by,
                user_id=request.user_id,
                password=request.password,
                admin_type=request.admin_type
            )

            self.db.add(new_admin)
            self.db.commit()
            self.db.refresh(new_admin)
            return new_admin
        except Exception as ex:
            _log.error("Unable to create admin record with user_id {}".format(request.user_id))
            raise FetchOneUserMetadataException(ex, request.user_id)

    def update_admin(self, request: AdminUser) -> AdminUser:
        try:
            existing_admin = self.db.query(AdminUser).filter(AdminUser.user_id == request.user_id).first()

            if not existing_admin:
                _log.info("No record found for admin with with user_id {}".format(AdminUser.user_id))
                return None

            setattr(existing_admin, 'password', request.password)
            setattr(existing_admin, 'admin_type', request.admin_type)

            self.db.commit()
            self.db.refresh(existing_admin)
            return existing_admin
        except Exception as ex:
            _log.error("Unable to update admin record with user_id {}".format(request.user_id))
            raise FetchOneUserMetadataException(ex, request.user_id)

    def delete_admin(self, user_id: str) -> AdminUser:
        try:
            existing_admin = self.db.query(AdminUser).filter(AdminUser.user_id == user_id).first()

            if not existing_admin:
                _log.info("No record found for admin with with user_id {}".format(user_id))
                return None

            self.db.delete(existing_admin)
            self.db.commit()
            return existing_admin
        except Exception as ex:
            _log.error("Unable to delete admin record with user_id {}".format(user_id))
            raise FetchOneUserMetadataException(ex, user_id)

    def get_admin_by_user_id(self, user_id: str) -> AdminUser:

        try:
            existing_admin = self.db.query(AdminUser).filter(AdminUser.user_id == user_id).first()
            if not existing_admin:
                _log.info("No record found for admin with with user_id {}".format(user_id))
                return None
            return existing_admin

        except Exception as ex:
            _log.error("Unable to fetch admin record with user_id {}".format(user_id))
            raise FetchOneUserMetadataException(ex, user_id)
