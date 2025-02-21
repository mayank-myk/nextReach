from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import func, desc
from sqlalchemy.orm import Session, aliased

from app.database.client_login_table import ClientLogin
from app.database.client_table import Client
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class ClientLoginRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_otp_by_phone_number(self, phone_number: str) -> Optional[List[ClientLogin]]:

        try:
            time_10_minutes_ago = datetime.utcnow() - timedelta(minutes=10)

            # Query for OTPs created in the last 10 minutes
            db_otp = self.db.query(ClientLogin).filter(
                ClientLogin.phone_number == phone_number,
                ClientLogin.created_at >= time_10_minutes_ago
            ).order_by(ClientLogin.created_at.desc()).all()

            if not db_otp:
                _log.info("No record found for otp with phone_number {}".format(phone_number))
                return None
            return db_otp

        except Exception as ex:
            raise FetchOneUserMetadataException(ex, phone_number)

    def save_otp_and_phone_number(self, otp: str, phone_number: str, otp_sent_successfully: bool) -> ClientLogin:
        try:
            db_otp = ClientLogin(
                otp=otp,
                phone_number=phone_number,
                sent_successfully=otp_sent_successfully
            )

            self.db.add(db_otp)
            self.db.commit()
            self.db.refresh(db_otp)
            return db_otp
        except Exception as ex:
            _log.error(f"Unable to create otp record for phone_number {phone_number}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, phone_number)

    def mark_otp_as_used(self, phone_number: str, otp: str) -> bool:
        """ Marks an OTP as used after successful validation. """
        try:
            otp_record = (
                self.db.query(ClientLogin)
                .filter(ClientLogin.phone_number == phone_number, ClientLogin.otp == otp, ClientLogin.success == False)
                .first()
            )

            if otp_record:
                otp_record.success = True
                self.db.commit()
                return True  # Successfully updated

            return False  # OTP not found or already used

        except Exception as ex:
            _log.error(f"Error marking OTP as used for phone_number {phone_number}. Error: {str(ex)}")
            return False  # Marking failed

    def save_otp_and_phone_number(self, otp: str, phone_number: str, otp_sent_successfully: bool) -> ClientLogin:
        try:
            db_otp = ClientLogin(
                otp=otp,
                phone_number=phone_number,
                sent_successfully=otp_sent_successfully
            )

            self.db.add(db_otp)
            self.db.commit()
            self.db.refresh(db_otp)
            return db_otp
        except Exception as ex:
            _log.error(f"Unable to create otp record for phone_number {phone_number}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, phone_number)

    def get_unique_logins(self):
        # Subquery: Get the first-ever login per phone number
        first_ever_login_subquery = (
            self.db.query(
                ClientLogin.phone_number.label("phone_number"),
                func.min(func.timezone('Asia/Kolkata', ClientLogin.created_at)).label("first_ever_login_time")
            )
            .group_by(ClientLogin.phone_number)
            .subquery()
        )

        # Subquery: Get the first login of the day for each phone number
        daily_first_login_subquery = (
            self.db.query(
                func.date(func.timezone('Asia/Kolkata', ClientLogin.created_at)).label("login_date"),
                # Extract the date
                ClientLogin.phone_number.label("phone_number"),
                func.min(func.timezone('Asia/Kolkata', ClientLogin.created_at)).label("first_login_time"),
                func.bool_or(ClientLogin.sent_successfully).label("otp_sent"),  # Check if any OTP was sent that day
                func.bool_or(ClientLogin.success).label("otp_validated")  # Check if any OTP was validated that day
            )
            .group_by(func.date(func.timezone('Asia/Kolkata', ClientLogin.created_at)), ClientLogin.phone_number)
            .subquery()
        )

        # Alias subqueries for better readability
        first_ever_login = aliased(first_ever_login_subquery)
        daily_first_login = aliased(daily_first_login_subquery)

        # Main Query: Determine if the user is "New" or "Old"
        query = (
            self.db.query(
                daily_first_login.c.login_date,
                daily_first_login.c.first_login_time,
                daily_first_login.c.phone_number,
                daily_first_login.c.otp_sent,
                daily_first_login.c.otp_validated,
                first_ever_login.c.first_ever_login_time,
                func.coalesce(Client.total_profile_visited, 0).label("total_profile_visited")
            )
            .join(
                first_ever_login,
                daily_first_login.c.phone_number == first_ever_login.c.phone_number
            )
            .outerjoin(Client, daily_first_login.c.phone_number == Client.phone_number)  # Join client table
            .order_by(desc(daily_first_login.c.login_date), desc(daily_first_login.c.first_login_time))
        )

        return query.all()
