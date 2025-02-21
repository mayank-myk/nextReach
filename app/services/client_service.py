from datetime import datetime
from io import BytesIO
from typing import List, Optional

import pandas as pd
from fastapi import BackgroundTasks

from app.api_requests.influencer_insights import InfluencerInsights
from app.api_requests.profile_update import ProfileUpdate
from app.clients.interakt_client import send_otp_via_whatsapp, collab_request_user_notification_via_whatsapp, \
    collab_request_admin_notification_via_whatsapp
from app.clients.meta_client import MetaAPIClient
from app.enums.average_view import AverageView
from app.enums.budget import Budget
from app.enums.campaign_stage import CampaignStage
from app.enums.city import City
from app.enums.collab_date import CollabDate
from app.enums.collab_type import CollabType
from app.enums.content_price import ContentPrice
from app.enums.engagement_rate import EngagementRate
from app.enums.follower_count import FollowerCount
from app.enums.gender import Gender
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform
from app.enums.rating import Rating
from app.enums.reach_price import ReachPrice
from app.enums.sort_applied import SortApplied
from app.repository.campaign_repository import CampaignRepository
from app.repository.client_login_repository import ClientLoginRepository
from app.repository.client_repository import ClientRepository
from app.repository.influencer_metric_repository import InfluencerMetricRepository
from app.repository.influencer_repository import InfluencerRepository
from app.repository.profile_visit_repository import ProfileVisitRepository
from app.response.campaign_review import CampaignReview
from app.response.client_profile import ClientProfile
from app.response.generic_response import GenericResponse
from app.response.influencer.facebook_detail import FacebookDetail
from app.response.influencer.influencer_collab_charge import InfluencerCollabCharge
from app.response.influencer.influencer_metric_detail import InfluencerMetricDetail
from app.response.influencer.influencer_review import InfluencerReview
from app.response.influencer.instagram_detail import InstagramDetail
from app.response.influencer.youtube_detail import YouTubeDetail
from app.response.influencer_basic_detail import InfluencerBasicDetail
from app.response.influencer_detail import InfluencerDetail
from app.response.influencer_listing import InfluencerListing
from app.response.login_response import LoginResponse
from app.response.new_singup_dump import NewSignupDump
from app.response.search_filter import SearchFilter
from app.utils import id_utils
from app.utils.converters import int_to_str_k, combine_names, format_to_rupees, format_to_views_charge, \
    city_distribution_to_dict, age_distribution_to_dict, sex_distribution_to_dict, float_to_str
from app.utils.logger import configure_logger

_log = configure_logger()


async def client_login_event(phone_number: str):
    try:
        meta_client = MetaAPIClient()
        await meta_client.send_event("Client Login", {
            "phone": phone_number,
            "custom_data": {"action": "client_login"},
            "event_source_url": "https://nextreach.ai/login_signup"
        })
    except Exception as ex:
        _log.error(f"Failed to push discovery event for {phone_number}: {str(ex)}")


async def influencer_discovery_event(phone_number: str):
    try:
        meta_client = MetaAPIClient()
        await meta_client.send_event("Discover Influencer", {
            "phone": phone_number,
            "custom_data": {"action": "influencer_discovery"},
            "event_source_url": "https://nextreach.ai/top_rated_influencers"
        })
    except Exception as ex:
        _log.error(f"Failed to push discovery event for {phone_number}: {str(ex)}")


class ClientService:
    def __init__(self, session):
        self.client_login_repository = ClientLoginRepository(session)
        self.client_repository = ClientRepository(session)
        self.campaign_repository = CampaignRepository(session)
        self.influencer_repository = InfluencerRepository(session)
        self.influencer_metric_repository = InfluencerMetricRepository(session)
        self.profile_visit_repository = ProfileVisitRepository(session)

    def get_client_profile(self, client_id: int) -> ClientProfile | GenericResponse:
        try:
            client_profile = self.client_repository.get_client_by_id(client_id=client_id)
            if client_profile:
                return ClientProfile(
                    id=client_profile.id,
                    phone_number=client_profile.phone_number,
                    name=client_profile.name,
                    business_name=client_profile.business_name,
                    email=client_profile.email,
                    city=client_profile.city,
                    niche=client_profile.niche,
                    category=client_profile.category,
                    total_profile_visited=client_profile.total_profile_visited,
                    balance_profile_visits=client_profile.balance_profile_visits,
                    insta_username=client_profile.insta_username,
                    yt_username=client_profile.yt_username,
                    fb_username=client_profile.fb_username)
            else:
                _log.info("No record found for client_profile with client_id: {}".format(client_id))
                return GenericResponse(success=False, button_text="Understood",
                                       message="No client profile found for given client_id")
        except Exception as e:
            _log.error(f"Error occurred while fetching profile for client_id: {client_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Try Again Later",
                                   message="Something went wrong while fetching client profile")

    def update_client_profile(self, client_id: int, profile: ProfileUpdate) -> GenericResponse:
        try:
            client_profile = self.client_repository.update_client_from_client(client_id=client_id, request=profile)
            if client_profile:
                return GenericResponse(success=True, button_text="Okay", header="Success!",
                                       message="User profile updated successfully")
            else:
                _log.info("No record found for client_profile with client_id: {}".format(client_id))
                return GenericResponse(success=False, button_text="Understood",
                                       message="No client profile found for given client_id")

        except Exception as e:
            _log.error(f"Error occurred while updating profile for client_id: {client_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Retry",
                                   message="Something went wrong while updating your profile")

    def send_otp(self, phone_number: str, background_tasks: BackgroundTasks) -> GenericResponse:
        background_tasks.add_task(client_login_event, phone_number)
        try:
            # login_record = self.client_login_repository.get_otp_by_phone_number(phone_number=phone_number)
            # if login_record:
            #     if (datetime.now() - login_record.created_at).total_seconds() < 600:
            #         return GenericResponse(success=True,
            #                                message="OTP has already been sent to this number, it's valid for 10minutes")
            otp = id_utils.generate_otp()
            otp_sent_successfully = send_otp_via_whatsapp(phone_number=phone_number, otp=otp)
            if not otp_sent_successfully:
                return GenericResponse(success=False, button_text="Retry",
                                       message="Failed to send OTP. Please ensure the number is a valid 10-digit WhatsApp number")

            self.client_login_repository.save_otp_and_phone_number(otp=otp, phone_number=phone_number)

            return GenericResponse(success=True, button_text="Okay", header="Success!",
                                   message="OTP has been successfully sent. Please check your WhatsApp")
        except Exception as ex:
            _log.error(f"Unable to create otp record for phone_number {phone_number}. Error: {str(ex)}")
            return GenericResponse(success=False, button_text="Try Again Later",
                                   message="Something went wrong while sending the OTP")

    def validate_otp(self, phone_number: str, otp: str) -> LoginResponse:

        login_records = self.client_login_repository.get_otp_by_phone_number(phone_number=phone_number)

        if not login_records or len(login_records) == 0:
            return LoginResponse(success=False, message="No OTP record found for the provided phone number",
                                 button_text="Understood", header="Oops!")

        otp_list = []
        for login_record in login_records:
            otp_list.append(login_record.otp)

        if otp in otp_list:
            client_record = self.client_repository.get_or_create_client_by_phone_number(phone_number=phone_number)
            return LoginResponse(client_id=client_record.id, success=True, header="Success!",
                                 message="OTP has been successfully verified", button_text="Proceed")
        else:
            return LoginResponse(success=False, header="Failed",
                                 message="Invalid OTP. It may have expired or doesn't match the latest one.",
                                 button_text="Get New OTP")

    def get_unique_logins(self):

        try:
            signup_records = self.client_login_repository.get_unique_logins()
            signup_detail_dump_list = []
            for record in signup_records:
                login_detail_dump = NewSignupDump(
                    login_date=record.login_date.strftime("%d-%m-%Y"),
                    first_login_time=record.first_login_time.strftime("%I:%M %p"),
                    phone_number=record.phone_number,
                    user_status=("New"
                                 if record.first_login_time == record.first_ever_login_time
                                 else "Old"
                                 )
                )
                signup_detail_dump_list.append(login_detail_dump)

                signup_data = [data.dict() for data in signup_detail_dump_list]

                # Create a DataFrame from the list of dictionaries
                df = pd.DataFrame(signup_data)

                # Save the DataFrame to a BytesIO buffer
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name=f'Signups_{datetime.today().strftime("%Y-%m-%d")}')
                buffer.seek(0)
            return buffer

        except Exception as e:
            _log.error(
                f"Error occurred while fetching campaigns details dump. Error: {str(e)}")

    def get_watchlist(self, client_id: int) -> List[InfluencerDetail]:

        pass

    def add_to_watchlist(self, client_id: int, influencer_id: int) -> GenericResponse:

        pass

    def remove_from_watchlist(self, client_id: int, influencer_id: int) -> GenericResponse:

        pass

    def request_collab(self, background_tasks: BackgroundTasks, created_by: str, client_id: int, influencer_id: int,
                       collab_date: Optional[CollabDate]) -> GenericResponse:

        try:
            all_collaboration_request_raised = self.campaign_repository.get_all_running_campaign_with_an_influencer(
                client_id=client_id, influencer_id=influencer_id)
            for request in all_collaboration_request_raised:
                if request.stage in [CampaignStage.CREATED, CampaignStage.INFLUENCER_FINALIZED,
                                     CampaignStage.SHOOT_COMPLETED,
                                     CampaignStage.CONTENT_POSTED, CampaignStage.DAY2_BILLING,
                                     CampaignStage.DAY8_BILLING]:
                    return GenericResponse(success=False, button_text="Understood",
                                           message="You already have an ongoing campaign with this influencer")

            influencer = self.influencer_repository.get_influencer_by_id(influencer_id=influencer_id)

            if influencer.primary_platform == Platform.FACEBOOK:
                influencer_metric = self.influencer_metric_repository.get_latest_influencer_fb_metric(
                    influencer_id=influencer_id)
            elif influencer.primary_platform == Platform.YOUTUBE:
                influencer_metric = self.influencer_metric_repository.get_latest_influencer_yt_metric(
                    influencer_id=influencer_id)
            else:
                influencer_metric = self.influencer_metric_repository.get_latest_influencer_insta_metric(
                    influencer_id=influencer_id)

            new_campaign = self.campaign_repository.create_collab_campaign(created_by=created_by,
                                                                           client_id=client_id, influencer=influencer,
                                                                           collab_date=collab_date)

            background_tasks.add_task(collab_request_user_notification_via_whatsapp, new_campaign.client.phone_number,
                                      datetime.today().strftime("%b %d, %Y"),
                                      influencer_metric.username, influencer.primary_platform,
                                      influencer_metric.profile_link,
                                      new_campaign.content_charge, new_campaign.views_charge,
                                      influencer_metric.followers, influencer_metric.avg_views)

            background_tasks.add_task(collab_request_admin_notification_via_whatsapp,
                                      datetime.today().strftime("%b %d, %Y"), str(new_campaign.id),
                                      str(new_campaign.client.id), str(influencer.id), new_campaign.client.name,
                                      new_campaign.client.phone_number, influencer_metric.username,
                                      influencer.phone_number, new_campaign.content_charge, new_campaign.views_charge,
                                      influencer_metric.followers, influencer_metric.avg_views)

            return GenericResponse(success=True, header="Success!", button_text="Thank You",
                                   message="Collaboration created successfully! Our team will reach out to you shortly")
        except Exception as e:
            _log.error(
                f"Error occurred while creating collaboration request for client_id: {client_id}, influencer_id: {influencer_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Try Again",
                                   message="Something went wrong while requesting collaboration")

    def check_if_profile_visited(self, client_id: int, influencer_id: int) -> bool:
        influencery_already_visited = self.profile_visit_repository.check_if_influencer_already_visited(client_id,
                                                                                                        influencer_id)
        if influencery_already_visited > 0:
            return True
        else:
            return False

    def track_profile_visit(self, client_id: int, influencer_id: int) -> bool:
        """
        Track a profile visit. If the client has reached the maximum number of visits allowed,
        the visit is not logged, and an error is raised.
        """
        influencery_already_visited = self.profile_visit_repository.check_if_influencer_already_visited(client_id,
                                                                                                        influencer_id)
        if influencery_already_visited > 0:
            _log.info(f"Profile already unlocked by client_id: {client_id} for influencer_id: {influencer_id}.")
            self.profile_visit_repository.log_already_visited_profile(client_id, influencer_id)
            return True

        client = self.client_repository.get_client_by_id(client_id)
        balance_profile_visit_count = client.balance_profile_visits

        if balance_profile_visit_count > 0:
            # Log the profile visit in the database
            self.profile_visit_repository.log_profile_visit(client_id, influencer_id)
            self.client_repository.update_profile_visit_count(client_id)
            _log.info(f"Profile visit successfully logged for client_id {client_id} to influencer_id: {influencer_id}.")
            return True
        else:
            _log.info(
                f"client_id: {client_id} has no balance left to visit influencer_id: {influencer_id}.")
            return False

    def influencer_to_influencer_basic_detail(self, matched_influencers, unmatched_influencers, client_id):

        influencer_ids = [influencer.id for influencer in matched_influencers] + [influencer.id for influencer in
                                                                                  unmatched_influencers]

        visited_profiles = set()
        if client_id and client_id != 1:
            visited_profiles = self.profile_visit_repository.get_all_influencers_visited(client_id=client_id,
                                                                                         influencer_ids=influencer_ids)

        latest_metrics = self.influencer_metric_repository.get_influencer_data_and_latest_metrics(
            influencer_ids=influencer_ids)
        metric_map = {metric.id: metric for metric in latest_metrics}

        matched_influencer_basic_detail_list = self.influencer_to_influencer_basic_detail_helper(matched_influencers,
                                                                                                 metric_map,
                                                                                                 visited_profiles)
        unmatched_influencer_basic_detail_list = self.influencer_to_influencer_basic_detail_helper(
            unmatched_influencers, metric_map, visited_profiles)

        return matched_influencer_basic_detail_list, unmatched_influencer_basic_detail_list

    def influencer_to_influencer_basic_detail_helper(self, influencers, metric_map, visited_profiles):

        influencer_basic_detail_list = []

        for influencer in influencers:
            influencer_metric = metric_map.get(influencer.id, None)

            if influencer_metric is None:
                continue

            if influencer.primary_platform == Platform.FACEBOOK:
                influencer_username = influencer_metric.fb_username
            elif influencer.primary_platform == Platform.YOUTUBE:
                influencer_username = influencer_metric.yt_username
            else:
                influencer_username = influencer_metric.insta_username

            if influencer_username is None:
                continue

            influencer_basic_detail = InfluencerBasicDetail(
                id=influencer.id,
                name=influencer_username,
                profile_picture=influencer.profile_picture,
                niche=influencer.niche,
                city=influencer.city,
                profile_visited=True if influencer.id in visited_profiles else False,
                views_charge=format_to_views_charge(influencer.views_charge),
                content_charge=format_to_rupees(influencer.content_charge),
                insta_followers=int_to_str_k(
                    influencer_metric.insta_followers) if influencer_metric.insta_followers else None,
                yt_followers=int_to_str_k(influencer_metric.yt_followers) if influencer_metric.yt_followers else None,
                fb_followers=int_to_str_k(influencer_metric.fb_followers) if influencer_metric.fb_followers else None
            )
            influencer_basic_detail_list.append(influencer_basic_detail)
        return influencer_basic_detail_list

    def get_influencer_listing(self, client_id: int,
                               page_number: int,
                               page_size: int,
                               sort_applied: SortApplied,
                               niche: Optional[List[Niche]],
                               city: Optional[City],
                               reach_price: Optional[List[ReachPrice]],
                               follower_count: Optional[List[FollowerCount]],
                               avg_views: Optional[List[AverageView]],
                               engagement: Optional[EngagementRate],
                               platform: Optional[Platform],
                               budget: Optional[Budget],
                               content_price: Optional[ContentPrice],
                               collab_type: Optional[CollabType],
                               gender: Optional[Gender],
                               rating: Optional[Rating],
                               languages: Optional[List[Language]],
                               background_tasks: BackgroundTasks
                               ) -> InfluencerListing:
        """
        Retrieve filtered influencer listings with latest metrics.
        """
        matched_influencers, all_matched_influencers = self.influencer_repository.filter_matched_influencers(
            page_number=page_number,
            page_size=page_size,
            sort_applied=sort_applied,
            niche=niche,
            city=city,
            reach_price=reach_price,
            follower_count=follower_count,
            avg_views=avg_views,
            engagement=engagement,
            platform=platform,
            budget=budget,
            content_price=content_price,
            collab_type=collab_type,
            gender=gender,
            rating=rating,
            language_list=languages
        )

        unmatched_influencers, all_unmatched_influencers = self.influencer_repository.filter_unmatched_influencers(
            matched_influencers,
            all_matched_influencers,
            page_number=page_number,
            page_size=page_size,
            sort_applied=sort_applied,
            niche=niche,
            city=city,
            reach_price=reach_price,
            follower_count=follower_count,
            avg_views=avg_views,
            engagement=engagement,
            platform=platform,
            budget=budget,
            content_price=content_price,
            collab_type=collab_type,
            gender=gender,
            rating=rating,
            language_list=languages
        )

        matched_influencer_basic_detail_list, unmatched_influencer_basic_detail_list = self.influencer_to_influencer_basic_detail(
            matched_influencers, unmatched_influencers, client_id)

        if client_id == 1:
            balance_profile_visit_count = 0
        else:
            client = self.client_repository.get_client_by_id(client_id)
            balance_profile_visit_count = client.balance_profile_visits
            background_tasks.add_task(influencer_discovery_event, client.phone_number)

        if (len(all_matched_influencers) + len(all_unmatched_influencers) - page_number * page_size) > 0:
            total_count_further_page = len(all_matched_influencers) + len(
                all_unmatched_influencers) - page_number * page_size
        else:
            total_count_further_page = 0

        total_count_current_page = len(matched_influencers) + len(unmatched_influencers)

        filters_applied = SearchFilter(
            niche=niche,
            city=city,
            reach_price=reach_price,
            follower_count=follower_count,
            avg_views=avg_views,
            engagement=engagement,
            platform=platform,
            budget=budget,
            content_price=content_price,
            gender=gender,
            collab_type=collab_type,
            rating=rating,
            languages=languages
        )

        return InfluencerListing(
            client_id=client_id,
            coin_balance=balance_profile_visit_count,
            matched_influencer_list=matched_influencer_basic_detail_list,
            unmatched_influencer_list=unmatched_influencer_basic_detail_list,
            filters_applied=filters_applied,
            sorting_applied=sort_applied,
            page_number=page_number,
            page_size=page_size,
            result_start_number=(page_number - 1) * page_size + 1 if total_count_current_page > 0 else 0,
            result_end_number=(page_number - 1) * page_size + len(matched_influencer_basic_detail_list) + len(
                unmatched_influencer_basic_detail_list) if total_count_current_page > 0 else 0,
            result_total_count=len(all_matched_influencers) + len(
                all_unmatched_influencers) if total_count_current_page > 0 else 0,
            result_count_further_page=total_count_further_page
        )

    def get_influencer_insight(self, request: InfluencerInsights) -> InfluencerDetail | GenericResponse:

        if request.client_id is None or request.client_id == 1:
            # return GenericResponse(success=False, button_text="Get Started Now", header="Login to Unlock Access",
            #                        message="Log in to unlock full influencer profiles and start collaborating, new users get 20 free coins!")

            return GenericResponse(success=False, button_text="One Step Signup", header="Signup & get 20 free coins",
                                   message="Use the coins to unlock influencer profiles & start collaboration instantly — Zero commissions, Zero upfront fees")

        try:

            influencer = self.influencer_repository.get_influencer_by_id(influencer_id=request.influencer_id)

            influencer_fb_metric = self.influencer_metric_repository.get_latest_influencer_fb_metric(
                influencer_id=request.influencer_id)
            influencer_yt_metric = self.influencer_metric_repository.get_latest_influencer_yt_metric(
                influencer_id=request.influencer_id)
            influencer_insta_metric = self.influencer_metric_repository.get_latest_influencer_insta_metric(
                influencer_id=request.influencer_id)

            if influencer.primary_platform == Platform.FACEBOOK:
                influencer_primary_metric = influencer_fb_metric
            elif influencer.primary_platform == Platform.YOUTUBE:
                influencer_primary_metric = influencer_yt_metric
            else:
                influencer_primary_metric = influencer_insta_metric

            if not influencer or not influencer_primary_metric:
                return GenericResponse(success=False, button_text="Understood", header="Failed",
                                       message="Something went wrong, unable to fetch complete details for the influencer")

            profile_visit_success = self.track_profile_visit(client_id=request.client_id,
                                                             influencer_id=request.influencer_id)

            if not profile_visit_success:
                return GenericResponse(success=False, button_text="Request Coins", header="Oops",
                                       message="Your coin balance is currently zero. Please recharge to view more profiles")

            instagram_detail = None
            if influencer_insta_metric:
                insta_city_graph = city_distribution_to_dict(
                    city_1=influencer_insta_metric.city_1,
                    city_pc_1=influencer_insta_metric.city_pc_1,
                    city_2=influencer_insta_metric.city_2,
                    city_pc_2=influencer_insta_metric.city_pc_2,
                    city_3=influencer_insta_metric.city_3,
                    city_pc_3=influencer_insta_metric.city_pc_3
                )

                insta_age_graph = age_distribution_to_dict(
                    age_13_to_17=influencer_insta_metric.age_13_to_17,
                    age_18_to_24=influencer_insta_metric.age_18_to_24,
                    age_25_to_34=influencer_insta_metric.age_25_to_34,
                    age_35_to_44=influencer_insta_metric.age_35_to_44,
                    age_45_to_54=influencer_insta_metric.age_45_to_54,
                    age_55=influencer_insta_metric.age_55
                )

                insta_sex_graph = sex_distribution_to_dict(
                    men_follower_pc=influencer_insta_metric.men_follower_pc,
                    women_follower_pc=influencer_insta_metric.women_follower_pc
                )

                instagram_detail = InstagramDetail(
                    id=influencer_insta_metric.id,
                    username=influencer_insta_metric.username,
                    profile_link=influencer_insta_metric.profile_link,
                    followers=int_to_str_k(influencer_insta_metric.followers),
                    avg_views=int_to_str_k(influencer_insta_metric.avg_views),
                    max_views=int_to_str_k(influencer_insta_metric.max_views),
                    min_views=int_to_str_k(influencer_insta_metric.min_views),
                    consistency_score=influencer_insta_metric.consistency_score,
                    avg_likes=int_to_str_k(influencer_insta_metric.avg_likes),
                    avg_comments=int_to_str_k(influencer_insta_metric.avg_comments),
                    avg_shares=int_to_str_k(influencer_insta_metric.avg_shares),
                    engagement_rate=float_to_str(influencer_insta_metric.engagement_rate),
                    city_graph=insta_city_graph,
                    age_graph=insta_age_graph,
                    sex_graph=insta_sex_graph
                )

            youtube_detail = None
            if influencer_yt_metric:
                yt_city_graph = city_distribution_to_dict(
                    city_1=influencer_yt_metric.city_1,
                    city_pc_1=influencer_yt_metric.city_pc_1,
                    city_2=influencer_yt_metric.city_2,
                    city_pc_2=influencer_yt_metric.city_pc_2,
                    city_3=influencer_yt_metric.city_3,
                    city_pc_3=influencer_yt_metric.city_pc_3
                )

                yt_age_graph = age_distribution_to_dict(
                    age_13_to_17=influencer_yt_metric.age_13_to_17,
                    age_18_to_24=influencer_yt_metric.age_18_to_24,
                    age_25_to_34=influencer_yt_metric.age_25_to_34,
                    age_35_to_44=influencer_yt_metric.age_35_to_44,
                    age_45_to_54=influencer_yt_metric.age_45_to_54,
                    age_55=influencer_yt_metric.age_55
                )

                yt_sex_graph = sex_distribution_to_dict(
                    men_follower_pc=influencer_yt_metric.men_follower_pc,
                    women_follower_pc=influencer_yt_metric.women_follower_pc
                )

                youtube_detail = YouTubeDetail(
                    id=influencer_yt_metric.id,
                    username=influencer_yt_metric.username,
                    profile_link=influencer_yt_metric.profile_link,
                    followers=int_to_str_k(influencer_yt_metric.followers),
                    avg_views=int_to_str_k(influencer_yt_metric.avg_views),
                    max_views=int_to_str_k(influencer_yt_metric.max_views),
                    min_views=int_to_str_k(influencer_yt_metric.min_views),
                    consistency_score=influencer_yt_metric.consistency_score,
                    avg_likes=int_to_str_k(influencer_yt_metric.avg_likes),
                    avg_comments=int_to_str_k(influencer_yt_metric.avg_comments),
                    avg_shares=int_to_str_k(influencer_yt_metric.avg_shares),
                    engagement_rate=float_to_str(influencer_yt_metric.engagement_rate),
                    city_graph=yt_city_graph,
                    age_graph=yt_age_graph,
                    sex_graph=yt_sex_graph
                )

            facebook_detail = None
            if influencer_fb_metric:
                fb_city_graph = city_distribution_to_dict(
                    city_1=influencer_fb_metric.city_1,
                    city_pc_1=influencer_fb_metric.city_pc_1,
                    city_2=influencer_fb_metric.city_2,
                    city_pc_2=influencer_fb_metric.city_pc_2,
                    city_3=influencer_fb_metric.city_3,
                    city_pc_3=influencer_fb_metric.city_pc_3
                )

                fb_age_graph = age_distribution_to_dict(
                    age_13_to_17=influencer_fb_metric.age_13_to_17,
                    age_18_to_24=influencer_fb_metric.age_18_to_24,
                    age_25_to_34=influencer_fb_metric.age_25_to_34,
                    age_35_to_44=influencer_fb_metric.age_35_to_44,
                    age_45_to_54=influencer_fb_metric.age_45_to_54,
                    age_55=influencer_fb_metric.age_55)

                fb_sex_graph = sex_distribution_to_dict(
                    men_follower_pc=influencer_fb_metric.men_follower_pc,
                    women_follower_pc=influencer_fb_metric.women_follower_pc
                )

                facebook_detail = FacebookDetail(
                    id=influencer_fb_metric.id,
                    username=influencer_fb_metric.username,
                    profile_link=influencer_fb_metric.profile_link,
                    followers=int_to_str_k(influencer_fb_metric.followers),
                    avg_views=int_to_str_k(influencer_fb_metric.avg_views),
                    max_views=int_to_str_k(influencer_fb_metric.max_views),
                    min_views=int_to_str_k(influencer_fb_metric.min_views),
                    consistency_score=influencer_fb_metric.consistency_score,
                    avg_likes=int_to_str_k(influencer_fb_metric.avg_likes),
                    avg_comments=int_to_str_k(influencer_fb_metric.avg_comments),
                    avg_shares=int_to_str_k(influencer_fb_metric.avg_shares),
                    engagement_rate=float_to_str(influencer_fb_metric.engagement_rate),
                    city_graph=fb_city_graph,
                    age_graph=fb_age_graph,
                    sex_graph=fb_sex_graph
                )

            platform_details = InfluencerMetricDetail(insta_detail=instagram_detail,
                                                      yt_detail=youtube_detail,
                                                      fb_detail=facebook_detail)

            collaboration_request_raised = False
            all_collaboration_request_raised = self.campaign_repository.get_all_running_campaign_with_an_influencer(
                client_id=request.client_id, influencer_id=request.influencer_id)
            for request in all_collaboration_request_raised:
                if request.stage in [CampaignStage.CREATED, CampaignStage.INFLUENCER_FINALIZED,
                                     CampaignStage.SHOOT_COMPLETED,
                                     CampaignStage.CONTENT_POSTED, CampaignStage.DAY2_BILLING,
                                     CampaignStage.DAY8_BILLING]:
                    collaboration_request_raised = True
                    continue

            all_campaign_for_an_influencer = self.campaign_repository.get_all_completed_campaign_for_an_influencer(
                influencer_id=request.influencer_id)
            campaign_review_list = []
            total_rating = 0
            for campaign in all_campaign_for_an_influencer:
                if campaign.rating:
                    total_rating += campaign.rating
                    campaign_review_list.append(CampaignReview(
                        user_name=combine_names(campaign.client.name, campaign.client.business_name),
                        rating=campaign.rating,
                        comment=campaign.review,
                        review_date=campaign.second_billing_date.strftime(
                            "%d %b %Y") if campaign.second_billing_date else None))

            if len(campaign_review_list) > 0:
                avg_rating = round(total_rating / len(campaign_review_list), 1)
                influencer_review = InfluencerReview(count=len(campaign_review_list),
                                                     avg_rating=f"{avg_rating}",
                                                     campaign_reviews=campaign_review_list)
            else:
                influencer_review = None

            return InfluencerDetail(
                id=influencer.id,
                last_updated_at=influencer.last_updated_at.strftime("%d %b %Y"),
                collaboration_ongoing=collaboration_request_raised,
                primary_platform=influencer.primary_platform,
                name=influencer.name,
                gender=influencer.gender,
                profile_picture=influencer.profile_picture,
                languages=uppercase_to_capitalized(influencer.languages),
                next_reach_score=influencer.next_reach_score,
                niche=influencer.niche,
                city=influencer.city,
                collab_type=influencer.collab_type,
                deliverables=influencer.deliverables,
                content_charge=format_to_rupees(influencer.content_charge),
                views_charge=format_to_views_charge(influencer.views_charge),
                collab_charge=get_collab_charge(influencer, influencer_primary_metric),
                platform_details=platform_details,
                influencer_review=influencer_review)

        except Exception as e:
            _log.error(
                f"Error occurred while fetching influencer details for influencer_id: {request.influencer_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Retry",
                                   message="Something went wrong while fetching influencer details")


def get_collab_charge(influencer, influencer_primary_metric) -> Optional[InfluencerCollabCharge]:
    if influencer.content_charge and influencer_primary_metric.avg_views and influencer_primary_metric.max_views and influencer.content_charge > 0 and influencer_primary_metric.avg_views > 0 and influencer_primary_metric.max_views > 0:
        return InfluencerCollabCharge(
            min=format_to_rupees(influencer.content_charge),
            avg=format_to_rupees(
                influencer.content_charge + (influencer_primary_metric.avg_views // 1000) * influencer.views_charge),
            max=format_to_rupees(
                influencer.content_charge + (influencer_primary_metric.max_views // 1000) * influencer.views_charge),
        )
    else:
        return None


def uppercase_to_capitalized(language_list):
    if language_list is None or len(language_list) == 0:
        return None

    output_list = []
    for language in language_list:
        words = language.value.lower().split("_")
        formatted_language = " ".join(words).capitalize()
        output_list.append(formatted_language)

    return output_list
