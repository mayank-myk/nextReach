from datetime import datetime
from typing import List

from app.database.client_table import Client
from app.repository.campaign_repository import CampaignRepository
from app.repository.client_repository import ClientRepository
from app.repository.user_login_repository import UserLoginRepository
from app.response.generic_response import GenericResponse
from app.requests.profile_update import ProfileUpdate
from app.response.influencer_detail import InfluencerDetail
from app.utils import id_utils
from app.utils.logger import configure_logger

_log = configure_logger()


class UserService:
    def __init__(self, session):
        self.user_login_repository = UserLoginRepository(session)
        self.client_repository = ClientRepository(session)
        self.campaign_repository = CampaignRepository(session)

    def get_user_profile(self, user_id: str) -> Client:
        try:
            return self.client_repository.get_client_by_id(client_id=user_id)
        except Exception as e:
            raise Exception(e)

    def update_user_profile(self, user_id: str, profile: ProfileUpdate) -> GenericResponse:
        try:
            self.client_repository.update_client_from_user(client_id=user_id, request=profile)
            return GenericResponse(success=True, error_code=None,
                                   error_message="User profile updated successfully")
        except Exception as e:
            return GenericResponse(success=False, error_code=None,
                                   error_message="User profile update failed")

    def send_otp(self, phone_number: str) -> GenericResponse:
        login_record = self.user_login_repository.get_otp_by_phone_number(phone_number=phone_number)
        if login_record:
            if (datetime.now() - login_record.created_at).total_seconds() < 3600:
                return GenericResponse(success=True, error_code=None,
                                       error_message="OTP has already been send to this number, and it is valid for 1hour")

        otp = id_utils.generate_otp()
        login_record = self.user_login_repository.save_otp_and_phone_number(otp=otp, phone_number=phone_number)

        if login_record:
            return GenericResponse(success=True, error_code=None, error_message="OTP has been sent successfully")
        else:
            return GenericResponse(success=False, error_code=None, error_message="Unable to send OTP")

    def validate_otp(self, phone_number: str, otp: str) -> GenericResponse:

        login_record = self.user_login_repository.get_otp_by_phone_number(phone_number=phone_number)
        if login_record:
            if login_record.otp == otp:
                return GenericResponse(success=True, error_code=None,
                                       error_message="OTP has been verified successfully")
            elif (datetime.now() - login_record.created_at).total_seconds() > 3600:
                return GenericResponse(success=True, error_code=None,
                                       error_message="OTP has expired, use the latest one or request resend OTP")
            else:
                return GenericResponse(success=False, error_code=None,
                                       error_message="Latest OTP which was sent to your registered mobile number does not matches with entered one")
        else:
            return GenericResponse(success=False, error_code=None,
                                   error_message="No OTP record found for this phone number")

    def get_watchlist(self, user_id: str) -> List[InfluencerDetail]:

        pass

    def add_to_watchlist(self, user_id: str, influencer_id: str) -> GenericResponse:

        pass

    def remove_from_watchlist(self, user_id: str, influencer_id: str) -> GenericResponse:

        pass

    def request_collab(self, user_id: str, influencer_id: str) -> GenericResponse:

        try:
            timestamp_id = id_utils.get_campaign_id()
            db_collab = self.campaign_repository.create_collab_campaign(campaign_id=timestamp_id, client_id=user_id,
                                                                        influencer_id=influencer_id)
            return GenericResponse(success=True, error_code=None,
                                   error_message="Collab created successfully, collab id {}".format(db_collab.id))
        except Exception as e:
            return GenericResponse(success=False, error_code=None,
                                   error_message="Collab creation failed")
