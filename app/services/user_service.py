from datetime import datetime
from typing import List

from app.api_requests.profile_update import ProfileUpdate
from app.clients.interakt_client import send_otp_via_whatsapp
from app.enums.campaign_stage import CampaignStage
from app.repository.campaign_repository import CampaignRepository
from app.repository.influencer_repository import InfluencerRepository
from app.repository.user_login_repository import UserLoginRepository
from app.repository.user_repository import UserRepository
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
        self.user_repository = UserRepository(session)
        self.campaign_repository = CampaignRepository(session)
        self.influencer_repository = InfluencerRepository(session)

    def get_user_profile(self, user_id: int) -> UserProfile | GenericResponse:
        try:
            user_profile = self.user_repository.get_user_by_id(user_id=user_id)
            if user_profile:
                return UserProfile(
                    id=user_profile.id,
                    phone_number=user_profile.phone_number,
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
                _log.info("No record found for user_profile with user_id: {}".format(user_id))
                return GenericResponse(success=False, button_text="Understood",
                                       message="No user profile found for given user_id")
        except Exception as e:
            _log.error(f"Error occurred while fetching profile for user_id: {user_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Try Again Later",
                                   message="Something went wrong while fetching user profile")

    def update_user_profile(self, user_id: int, profile: ProfileUpdate) -> GenericResponse:
        try:
            user_profile = self.user_repository.update_user_from_user(user_id=user_id, request=profile)
            if user_profile:
                return GenericResponse(success=True, button_text="Okay", header="Success!",
                                       message="User profile updated successfully")
            else:
                _log.info("No record found for user_profile with user_id: {}".format(user_id))
                return GenericResponse(success=False, button_text="Understood",
                                       message="No user profile found for given user_id")

        except Exception as e:
            _log.error(f"Error occurred while updating profile for user_id: {user_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Retry",
                                   message="Something went wrong while updating your profile")

    def send_otp(self, phone_number: str) -> GenericResponse:
        try:
            # login_record = self.user_login_repository.get_otp_by_phone_number(phone_number=phone_number)
            # if login_record:
            #     if (datetime.now() - login_record.created_at).total_seconds() < 600:
            #         return GenericResponse(success=True,
            #                                message="OTP has already been send to this number, it's valid for 10minutes")
            otp = id_utils.generate_otp()
            otp_sent_successfully = send_otp_via_whatsapp(phone_number=phone_number, otp=otp)
            if not otp_sent_successfully:
                return GenericResponse(success=False, button_text="Retry",
                                       message="Failed to send OTP. Please ensure the number is a valid 10-digit WhatsApp number")

            login_record = self.user_login_repository.save_otp_and_phone_number(otp=otp, phone_number=phone_number)

            return GenericResponse(success=True, button_text="Okay", header="Success!",
                                   message="OTP has been successfully sent. Please check your WhatsApp")
        except Exception as ex:
            _log.error(f"Unable to create otp record for phone_number {phone_number}. Error: {str(ex)}")
            return GenericResponse(success=False, button_text="Try Again Later",
                                   message="Something went wrong while sending the OTP")

    def validate_otp(self, phone_number: str, otp: str) -> LoginResponse:

        login_record = self.user_login_repository.get_otp_by_phone_number(phone_number=phone_number)
        if login_record:
            if login_record.otp == otp:
                user_record = self.user_repository.get_or_create_user_by_phone_number(phone_number=phone_number)
                return LoginResponse(user_id=user_record.id, success=True, header="Success!",
                                     message="OTP has been successfully verified", button_text="Proceed")
            elif (datetime.now() - login_record.created_at).total_seconds() > 600:
                return LoginResponse(success=False,
                                     message="OTP has expired. Please use the latest one or request a new OTP",
                                     button_text="Retry")
            else:
                return LoginResponse(success=False, button_text="Try Again",
                                     message="The OTP you entered doesn't match the latest one sent to your registered mobile number")
        else:
            return LoginResponse(success=False, message="No OTP record found for the provided phone number",
                                 button_text="Understood")

    def get_watchlist(self, user_id: int) -> List[InfluencerDetail]:

        pass

    def add_to_watchlist(self, user_id: int, influencer_id: int) -> GenericResponse:

        pass

    def remove_from_watchlist(self, user_id: int, influencer_id: int) -> GenericResponse:

        pass

    def request_collab(self, user_id: int, influencer_id: int) -> GenericResponse:

        try:
            all_collaboration_request_raised = self.campaign_repository.get_all_running_campaign_with_an_influencer(
                user_id=user_id, influencer_id=influencer_id)
            for request in all_collaboration_request_raised:
                if request.stage in [CampaignStage.CREATED, CampaignStage.INFLUENCER_FINALIZATION,
                                     CampaignStage.SHOOT,
                                     CampaignStage.POST, CampaignStage.FIRST_BILLING, CampaignStage.SECOND_BILLING]:
                    return GenericResponse(success=False, button_text="Understood",
                                           message="You already have an ongoing campaign with this influencer")

            influencer = self.influencer_repository.get_influencer_by_id(influencer_id=influencer_id)
            db_collab = self.campaign_repository.create_collab_campaign(user_id=user_id, influencer=influencer)

            return GenericResponse(success=True, header="Success!", button_text="Thank You",
                                   message="Collaboration created successfully! Our team will reach out to you shortly")
        except Exception as e:
            _log.error(
                f"Error occurred while creating collaboration request for user_id: {user_id}, influencer_id: {influencer_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Try Again",
                                   message="Something went wrong while requesting collaboration")
