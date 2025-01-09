from datetime import datetime
from typing import List, Optional

from app.api_requests.influencer_insights import InfluencerInsights
from app.api_requests.profile_update import ProfileUpdate
from app.clients.interakt_client import send_otp_via_whatsapp
from app.database.influencer_metric_table import InfluencerMetric
from app.database.influencer_table import Influencer
from app.enums.average_view import AverageView
from app.enums.campaign_stage import CampaignStage
from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.content_price import ContentPrice
from app.enums.engagement_rate import EngagementRate
from app.enums.follower_count import FollowerCount
from app.enums.gender import Gender
from app.enums.influencer_age import InfluencerAge
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform
from app.enums.rating import Rating
from app.enums.reach_price import ReachPrice
from app.enums.sort_applied import SortApplied
from app.repository.campaign_repository import CampaignRepository
from app.repository.influencer_repository import InfluencerRepository
from app.repository.profile_visit_repository import ProfileVisitRepository
from app.repository.user_login_repository import UserLoginRepository
from app.repository.user_repository import UserRepository
from app.response.campaign_review import CampaignReview
from app.response.generic_response import GenericResponse
from app.response.influencer.age_distribution_graph import AgeDistributionGraph
from app.response.influencer.city_distribution_graph import CityDistributionGraph
from app.response.influencer.facebook_detail import FacebookDetail
from app.response.influencer.influencer_collab_charge import InfluencerCollabCharge
from app.response.influencer.influencer_metric_detail import InfluencerMetricDetail
from app.response.influencer.influencer_review import InfluencerReview
from app.response.influencer.instagram_detail import InstagramDetail
from app.response.influencer.sex_distribution_graph import SexDistributionGraph
from app.response.influencer.youtube_detail import YouTubeDetail
from app.response.influencer_basic_detail import InfluencerBasicDetail
from app.response.influencer_detail import InfluencerDetail
from app.response.influencer_listing import InfluencerListing
from app.response.login_response import LoginResponse
from app.response.search_filter import SearchFilter
from app.response.user_profile import UserProfile
from app.utils import id_utils
from app.utils.converters import int_to_str_k, combine_names
from app.utils.logger import configure_logger

_log = configure_logger()


class UserService:
    def __init__(self, session):
        self.user_login_repository = UserLoginRepository(session)
        self.user_repository = UserRepository(session)
        self.campaign_repository = CampaignRepository(session)
        self.influencer_repository = InfluencerRepository(session)
        self.profile_visit_repository = ProfileVisitRepository(session)

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
            #                                message="OTP has already been sent to this number, it's valid for 10minutes")
            otp = id_utils.generate_otp()
            otp_sent_successfully = send_otp_via_whatsapp(phone_number=phone_number, otp=otp)
            if not otp_sent_successfully:
                return GenericResponse(success=False, button_text="Retry",
                                       message="Failed to send OTP. Please ensure the number is a valid 10-digit WhatsApp number")

            self.user_login_repository.save_otp_and_phone_number(otp=otp, phone_number=phone_number)

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
            self.campaign_repository.create_collab_campaign(user_id=user_id, influencer=influencer)

            return GenericResponse(success=True, header="Success!", button_text="Thank You",
                                   message="Collaboration created successfully! Our team will reach out to you shortly")
        except Exception as e:
            _log.error(
                f"Error occurred while creating collaboration request for user_id: {user_id}, influencer_id: {influencer_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Try Again",
                                   message="Something went wrong while requesting collaboration")

    def check_if_profile_visited(self, user_id: int, influencer_id: int) -> bool:
        influencery_already_visited = self.profile_visit_repository.check_if_influencer_already_visited(user_id,
                                                                                                        influencer_id)
        if influencery_already_visited > 0:
            return True
        else:
            return False

    def track_profile_visit(self, user_id: int, influencer_id: int) -> bool:
        """
        Track a profile visit. If the user has reached the maximum number of visits allowed,
        the visit is not logged, and an error is raised.
        """
        influencery_already_visited = self.profile_visit_repository.check_if_influencer_already_visited(user_id,
                                                                                                        influencer_id)
        if influencery_already_visited > 0:
            _log.info(f"Profile already unlocked by user_id: {user_id} for influencer_id: {influencer_id}.")
            self.profile_visit_repository.log_already_visited_profile(user_id, influencer_id)
            return True

        user = self.user_repository.get_user_by_id(user_id)
        balance_profile_visit_count = user.balance_profile_visits

        if balance_profile_visit_count > 0:
            # Log the profile visit in the database
            self.profile_visit_repository.log_profile_visit(user_id, influencer_id)
            self.user_repository.update_profile_visit_count(user_id)
            _log.info(f"Profile visit successfully logged for user_id {user_id} to influencer_id: {influencer_id}.")
            return True
        else:
            _log.info(
                f"user_id {user_id} has no balance left to visit influencer_id: {influencer_id}.")
            return False

    def influencer_to_influencer_basic_detail(self, influencers, user_id):

        influencer_basic_detail_list = []
        for influencer in influencers:
            latest_metric = max(influencer.influencer_metric, key=lambda m: m.created_at, default=None)
            influencer_basic_detail = InfluencerBasicDetail(
                id=influencer.id,
                name=influencer.name,
                profile_picture=influencer.profile_picture,
                niche=influencer.niche,
                city=influencer.city,
                profile_visited=self.check_if_profile_visited(user_id=user_id, influencer_id=influencer.id),
                views_charge=influencer.views_charge,
                content_charge=influencer.content_charge,
                insta_followers=int_to_str_k(latest_metric.insta_followers) if latest_metric else 0,
                yt_followers=int_to_str_k(latest_metric.yt_followers) if latest_metric else 0,
            )
            influencer_basic_detail_list.append(influencer_basic_detail)
        return influencer_basic_detail_list

    def get_influencer_listing(self, user_id: int,
                               page_number: int,
                               page_size: int,
                               sort_applied: SortApplied,
                               niche: Optional[List[Niche]],
                               city: Optional[List[City]],
                               reach_price: Optional[List[ReachPrice]],
                               follower_count: Optional[List[FollowerCount]],
                               avg_views: Optional[List[AverageView]],
                               engagement: Optional[EngagementRate],
                               platform: Optional[Platform],
                               content_price: Optional[ContentPrice],
                               collab_type: Optional[CollabType],
                               gender: Optional[List[Gender]],
                               age: Optional[List[InfluencerAge]],
                               rating: Optional[Rating],
                               languages: Optional[List[Language]]
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
            content_price=content_price,
            collab_type=collab_type,
            gender=gender,
            influencer_age=age,
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
            content_price=content_price,
            collab_type=collab_type,
            gender=gender,
            influencer_age=age,
            rating=rating,
            language_list=languages
        )

        matched_influencer_basic_detail_list = self.influencer_to_influencer_basic_detail(matched_influencers, user_id)
        unmatched_influencer_basic_detail_list = self.influencer_to_influencer_basic_detail(unmatched_influencers,
                                                                                            user_id)

        user = self.user_repository.get_user_by_id(user_id)
        balance_profile_visit_count = user.balance_profile_visits
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
            content_price=content_price,
            gender=gender,
            collab_type=collab_type,
            age=age,
            rating=rating,
            languages=languages
        )

        return InfluencerListing(
            user_id=user_id,
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
        try:

            influencer = self.influencer_repository.get_influencer_by_id(influencer_id=request.influencer_id)
            influencer_metric = self.influencer_repository.get_latest_influencer_metric(
                influencer_id=request.influencer_id)

            if not influencer or not influencer_metric:
                return GenericResponse(success=False, button_text="Understood", header="Failed",
                                       message="Something went wrong, unable to fetch complete details for the influencer")

            profile_visit_success = self.track_profile_visit(user_id=request.user_id,
                                                             influencer_id=request.influencer_id)

            if not profile_visit_success:
                return GenericResponse(success=False, button_text="Request Coins", header="Oops",
                                       message="Your coin balance is currently zero. Please recharge to view more profiles")

            instagram_detail = None
            if influencer.insta_username:
                insta_city_graph = None
                if influencer_metric.insta_city_1 and influencer_metric.insta_city_2 and influencer_metric.insta_city_3:
                    insta_city_graph = CityDistributionGraph(
                        city_1=influencer_metric.insta_city_1,
                        city_pc_1=influencer_metric.insta_city_pc_1,
                        city_2=influencer_metric.insta_city_2,
                        city_pc_2=influencer_metric.insta_city_pc_2,
                        city_3=influencer_metric.insta_city_3,
                        city_pc_3=influencer_metric.insta_city_pc_3
                    )

                insta_age_graph = None
                if influencer_metric.insta_age_13_to_17 > 0 or influencer_metric.insta_age_18_to_24 > 0 or influencer_metric.insta_age_25_to_34 > 0 or influencer_metric.insta_age_35_to_44 > 0 or influencer_metric.insta_age_45_to_54 > 0 or influencer_metric.insta_age_55 > 0:
                    insta_age_graph = AgeDistributionGraph(
                        age_13_to_17=influencer_metric.insta_age_13_to_17,
                        age_18_to_24=influencer_metric.insta_age_18_to_24,
                        age_25_to_34=influencer_metric.insta_age_25_to_34,
                        age_35_to_44=influencer_metric.insta_age_35_to_44,
                        age_45_to_54=influencer_metric.insta_age_45_to_54,
                        age_55=influencer_metric.insta_age_55
                    )

                insta_sex_graph = SexDistributionGraph(
                    men_follower_pc=influencer_metric.insta_men_follower_pc,
                    women_follower_pc=influencer_metric.insta_women_follower_pc
                )

                instagram_detail = InstagramDetail(
                    username=influencer.insta_username,
                    followers=int_to_str_k(influencer_metric.insta_followers),
                    city_graph=insta_city_graph,
                    age_graph=insta_age_graph,
                    sex_graph=insta_sex_graph,
                    avg_views=int_to_str_k(influencer_metric.insta_avg_views),
                    max_views=int_to_str_k(influencer_metric.insta_max_views),
                    min_views=int_to_str_k(influencer_metric.insta_min_views),
                    consistency_score=influencer_metric.insta_consistency_score,
                    avg_likes=int_to_str_k(influencer_metric.insta_avg_likes),
                    avg_comments=int_to_str_k(influencer_metric.insta_avg_comments),
                    avg_shares=int_to_str_k(influencer_metric.insta_avg_shares),
                    engagement_rate=influencer_metric.insta_engagement_rate
                )

            youtube_detail = None
            if influencer.yt_username:

                yt_city_graph = None
                if influencer_metric.yt_city_1 and influencer_metric.yt_city_2 and influencer_metric.yt_city_3:
                    yt_city_graph = CityDistributionGraph(
                        city_1=influencer_metric.yt_city_1,
                        city_pc_1=influencer_metric.yt_city_pc_1,
                        city_2=influencer_metric.yt_city_2,
                        city_pc_2=influencer_metric.yt_city_pc_2,
                        city_3=influencer_metric.yt_city_3,
                        city_pc_3=influencer_metric.yt_city_pc_3
                    )

                youtube_detail = YouTubeDetail(
                    username=influencer.yt_username,
                    followers=int_to_str_k(influencer_metric.yt_followers),
                    city_graph=yt_city_graph,
                    avg_views=int_to_str_k(influencer_metric.yt_avg_views),
                    max_views=int_to_str_k(influencer_metric.yt_max_views),
                    min_views=int_to_str_k(influencer_metric.yt_min_views),
                    consistency_score=influencer_metric.yt_consistency_score,
                    avg_likes=int_to_str_k(influencer_metric.yt_avg_likes),
                    avg_comments=int_to_str_k(influencer_metric.yt_avg_comments),
                    avg_shares=int_to_str_k(influencer_metric.yt_avg_shares),
                    engagement_rate=influencer_metric.yt_engagement_rate
                )

            facebook_detail = None
            if influencer.fb_username:

                fb_city_graph = None
                if influencer_metric.fb_city_1 and influencer_metric.fb_city_2 and influencer_metric.fb_city_3:
                    fb_city_graph = CityDistributionGraph(
                        city_1=influencer_metric.fb_city_1,
                        city_pc_1=influencer_metric.fb_city_pc_1,
                        city_2=influencer_metric.fb_city_2,
                        city_pc_2=influencer_metric.fb_city_pc_2,
                        city_3=influencer_metric.fb_city_3,
                        city_pc_3=influencer_metric.fb_city_pc_3
                    )

                facebook_detail = FacebookDetail(
                    username=influencer.fb_username,
                    followers=int_to_str_k(influencer_metric.fb_followers),
                    city_graph=fb_city_graph,
                    avg_views=int_to_str_k(influencer_metric.fb_avg_views),
                    max_views=int_to_str_k(influencer_metric.fb_max_views),
                    min_views=int_to_str_k(influencer_metric.fb_min_views),
                    consistency_score=influencer_metric.fb_consistency_score,
                    avg_likes=int_to_str_k(influencer_metric.fb_avg_likes),
                    avg_comments=int_to_str_k(influencer_metric.fb_avg_comments),
                    avg_shares=int_to_str_k(influencer_metric.fb_avg_shares),
                    engagement_rate=influencer_metric.fb_engagement_rate
                )

            platform_details = InfluencerMetricDetail(insta_detail=instagram_detail,
                                                      yt_detail=youtube_detail,
                                                      fb_detail=facebook_detail)

            collaboration_request_raised = False
            all_collaboration_request_raised = self.campaign_repository.get_all_running_campaign_with_an_influencer(
                user_id=request.user_id, influencer_id=request.influencer_id)
            for request in all_collaboration_request_raised:
                if request.stage in [CampaignStage.CREATED, CampaignStage.INFLUENCER_FINALIZATION, CampaignStage.SHOOT,
                                     CampaignStage.POST, CampaignStage.FIRST_BILLING, CampaignStage.SECOND_BILLING]:
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
                        user_name=combine_names(campaign.user.name, campaign.user.business_name),
                        rating=campaign.rating,
                        comment=campaign.review,
                        review_date=campaign.second_billing_date.strftime(
                            "%d %b %Y") if campaign.second_billing_date else None))

            if len(campaign_review_list) > 0:
                avg_rating = total_rating / len(campaign_review_list)
                influencer_review = InfluencerReview(count=len(campaign_review_list),
                                                     avg_rating=f"{avg_rating:.1f}",
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
                languages=influencer.languages,
                age=influencer.age,
                next_reach_score=influencer.next_reach_score,
                niche=influencer.niche,
                city=influencer.city,
                collab_type=influencer.collab_type,
                deliverables=influencer.deliverables,
                content_charge=influencer.content_charge,
                views_charge=influencer.views_charge,
                collab_charge=get_collab_charge(influencer, influencer_metric),
                platform_details=platform_details,
                influencer_review=influencer_review)

        except Exception as e:
            _log.error(
                f"Error occurred while fetching influencer details for influencer_id: {request.influencer_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Retry",
                                   message="Something went wrong while fetching influencer details")


def get_collab_charge(influencer: Influencer, influencer_metric: InfluencerMetric) -> Optional[InfluencerCollabCharge]:
    if influencer.content_charge == 0 or influencer.views_charge == 0:
        return None

    if influencer.primary_platform == Platform.INSTAGRAM:
        if influencer_metric.insta_avg_views == 0 or influencer_metric.insta_max_views == 0:
            return None
        else:
            return InfluencerCollabCharge(
                min=influencer.content_charge,
                avg=(influencer_metric.insta_avg_views // 1000) * influencer.views_charge,
                max=(influencer_metric.insta_max_views // 1000) * influencer.views_charge,
            )

    if influencer.primary_platform == Platform.YOUTUBE:
        if influencer_metric.yt_avg_views == 0 or influencer_metric.yt_max_views == 0:
            return None
        else:
            return InfluencerCollabCharge(
                min=influencer.content_charge,
                avg=(influencer_metric.yt_avg_views // 1000) * influencer.views_charge,
                max=(influencer_metric.yt_max_views // 1000) * influencer.views_charge,
            )

    if influencer.primary_platform == Platform.FACEBOOK:
        if influencer_metric.fb_avg_views == 0 or influencer_metric.fb_max_views == 0:
            return None
        else:
            return InfluencerCollabCharge(
                min=influencer.content_charge,
                avg=(influencer_metric.fb_avg_views // 1000) * influencer.views_charge,
                max=(influencer_metric.fb_max_views // 1000) * influencer.views_charge,
            )
    return None
