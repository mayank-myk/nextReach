from typing import Optional
from sqlalchemy.orm import Session
from app.database.user_login_table import UserLogin
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class UserLoginRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_otp_by_phone_number(self, phone_number: str) -> Optional[UserLogin]:

        try:
            db_otp = self.db.query(UserLogin).filter(UserLogin.phone_number == phone_number).order_by(
                UserLogin.created_at.desc()).first()

            if not db_otp:
                _log.info("No record found for otp with phone_number {}".format(phone_number))
                return None
            return db_otp

        except Exception as ex:
            raise FetchOneUserMetadataException(ex, phone_number)

    def save_otp_and_phone_number(self, otp: str, phone_number: str) -> UserLogin:
        try:
            db_otp = UserLogin(
                otp=otp,
                phone_number=phone_number,
            )

            self.db.add(db_otp)
            self.db.commit()
            self.db.refresh(db_otp)
            return db_otp
        except Exception as ex:
            _log.error("Unable to create otp record for phone_number {}".format(phone_number))
            raise FetchOneUserMetadataException(ex, phone_number)
