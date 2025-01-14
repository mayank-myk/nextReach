from typing import Optional

from sqlalchemy.orm import Session

from app.database.client_login_table import ClientLogin
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class ClientLoginRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_otp_by_phone_number(self, phone_number: str) -> Optional[ClientLogin]:

        try:
            db_otp = self.db.query(ClientLogin).filter(ClientLogin.phone_number == phone_number).order_by(
                ClientLogin.created_at.desc()).first()

            if not db_otp:
                _log.info("No record found for otp with phone_number {}".format(phone_number))
                return None
            return db_otp

        except Exception as ex:
            raise FetchOneUserMetadataException(ex, phone_number)

    def save_otp_and_phone_number(self, otp: str, phone_number: str) -> ClientLogin:
        try:
            db_otp = ClientLogin(
                otp=otp,
                phone_number=phone_number,
            )

            self.db.add(db_otp)
            self.db.commit()
            self.db.refresh(db_otp)
            return db_otp
        except Exception as ex:
            _log.error(f"Unable to create otp record for phone_number {phone_number}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, phone_number)
