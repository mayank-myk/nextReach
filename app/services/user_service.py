from datetime import datetime
from typing import List

from app.repository.campaign_repository import CampaignRepository
from app.repository.client_repository import ClientRepository
from app.repository.user_login_repository import UserLoginRepository
from app.requests.profile_update import ProfileUpdate
from app.response.generic_response import GenericResponse
from app.response.influencer_detail import InfluencerDetail
from app.response.login_response import LoginResponse
from app.response.user_profile import UserProfile
from app.utils import id_utils
from app.utils.logger import configure_logger

_log = configure_logger()


class UserService:
    def __init__(self, session):
        self.user_login_repository = UserLoginRepository(session)
        self.client_repository = ClientRepository(session)
        self.campaign_repository = CampaignRepository(session)

    def get_user_profile(self, user_id: str) -> UserProfile | GenericResponse:
        try:
            user_profile = self.client_repository.get_client_by_id(client_id=user_id)
            if user_profile:
                return UserProfile(
                    id=user_profile.id,
                    name=user_profile.name,
                    business_name=user_profile.business_name,
                    email=user_profile.email,
                    city=user_profile.city,
                    niche=user_profile.niche,
                    category=user_profile.category,
                    total_profile_visited=user_profile.total_profile_visited,
                    balance_profile_visits=user_profile.balance_profile_visits,
                    insta_username=user_profile.insta_username,
                    yt_username=user_profile.yt_username,
                    fb_username=user_profile.fb_username)
            else:
                _log.info("No record found for user_profile with user_id {}".format(user_id))
                return GenericResponse(success=False, button_text=None,
                                       message="No user profile found for given user_id")
        except Exception as e:
            _log.error(f"Error occurred while fetching profile for user_id: {user_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text=None,
                                   message="Something went wrong while fetching user profile")

    def update_user_profile(self, user_id: str, profile: ProfileUpdate) -> GenericResponse:
        try:
            user_profile = self.client_repository.update_client_from_user(client_id=user_id, request=profile)
            if user_profile:
                return GenericResponse(success=True, button_text=None,
                                       message="User profile updated successfully")
            else:
                _log.info("No record found for user_profile with user_id {}".format(user_id))
                return GenericResponse(success=False, button_text=None,
                                       message="No user profile found for given user_id")

        except Exception as e:
            _log.error(f"Error occurred while updating profile for user_id: {user_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text=None,
                                   message="Something went wrong while updating your profile")

    def send_otp(self, phone_number: str) -> GenericResponse:
        login_record = self.user_login_repository.get_otp_by_phone_number(phone_number=phone_number)
        if login_record:
            if (datetime.now() - login_record.created_at).total_seconds() < 3600:
                return GenericResponse(success=True, button_text=None,
                                       message="OTP has already been send to this number, and it is valid for 1hour")

        otp = id_utils.generate_otp()
        login_record = self.user_login_repository.save_otp_and_phone_number(otp=otp, phone_number=phone_number)

        if login_record:
            return GenericResponse(success=True, button_text=None, message="OTP has been sent successfully")
        else:
            return GenericResponse(success=False, button_text=None, message="Unable to send OTP")

    def validate_otp(self, phone_number: str, otp: str) -> LoginResponse:

        login_record = self.user_login_repository.get_otp_by_phone_number(phone_number=phone_number)
        client_record = self.client_repository.get_client_by_phone_number(phone_number=phone_number)
        if login_record:
            if login_record.otp == otp:
                return LoginResponse(user_id=client_record.id, success=True,
                                     message="OTP has been verified successfully")
            elif (datetime.now() - login_record.created_at).total_seconds() > 3600:
                return LoginResponse(success=False, message="OTP has expired, use the latest one or request resend OTP")
            else:
                return LoginResponse(success=False,
                                     message="Latest OTP which was sent to your registered mobile number does not matches with entered one")
        else:
            return LoginResponse(success=False, message="No OTP record found for this phone number")

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
            return GenericResponse(success=True, button_text=None,
                                   message="Collab created successfully, Our team will get back to you soon")
        except Exception as e:
            _log.error(
                f"Error occurred while creating collaboration request for user_id: {user_id}, influencer_id: {influencer_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text=None,
                                   message="Collaboration request failed, please retry")
