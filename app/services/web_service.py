from typing import Optional, List

from app.api_requests.influencer_insights import InfluencerInsights
from app.api_requests.waitlist_request import WaitListRequest
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
from app.repository.user_repository import UserRepository
from app.repository.wait_list_repository import WaitListRepository
from app.response.facebook_detail import FacebookDetail
from app.response.generic_response import GenericResponse
from app.response.influencer_basic_detail import InfluencerBasicDetail
from app.response.influencer_collab_charge import InfluencerCollabCharge
from app.response.influencer_detail import InfluencerDetail
from app.response.influencer_listing import InfluencerListing
from app.response.influencer_metric_detail import InfluencerMetricDetail
from app.response.instagram_detail import InstagramDetail
from app.response.search_filter import SearchFilter
from app.response.youtube_detail import YouTubeDetail
from app.utils.converters import int_to_str_k
from app.utils.logger import configure_logger

_log = configure_logger()


class WebService:
    def __init__(self, session):
        self.influencer_repository = InfluencerRepository(session)
        self.wait_list_user_repository = WaitListRepository(session)
        self.profile_visit_repository = ProfileVisitRepository(session)
        self.user_repository = UserRepository(session)
        self.campaign_repository = CampaignRepository(session)

    def get_web_metadata(self) -> GenericResponse:
        pass

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

    def get_influencer_listing(self, user_id: int,
                               page_number: int,
                               page_size: int,
                               sort_applied: Optional[SortApplied],
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
        influencers = self.influencer_repository.filter_influencers(
            page_number=page_number,
            page_size=page_size,
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
            languages=languages
        )

        influencer_basic_detail_list = []
        for influencer in influencers:
            latest_metric = max(influencer.influencer_metric, key=lambda m: m.created_at, default=None)
            influencer_basic_detail = InfluencerBasicDetail(
                id=influencer.id,
                name=influencer.name,
                profile_picture=influencer.profile_picture,
                niche=influencer.niche,
                city=influencer.city,
                profile_visited=False,
                views_charge=influencer.views_charge,
                content_charge=influencer.content_charge,
                instagram_followers=int_to_str_k(latest_metric.insta_followers) if latest_metric else 0,
                youtube_followers=int_to_str_k(latest_metric.yt_followers) if latest_metric else 0,
            )
            influencer_basic_detail_list.append(influencer_basic_detail)

        user = self.user_repository.get_user_by_id(user_id)
        balance_profile_visit_count = user.balance_profile_visits

        return InfluencerListing(
            user_id=user_id,
            coin_balance=balance_profile_visit_count,
            influencer_list=influencer_basic_detail_list,
            filters_applied=SearchFilter(
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
            ),
            sorting_applied=sort_applied,
            page_number=page_number,
            page_size=page_size,
            total_match_number=len(influencer_basic_detail_list)
        )

    def get_influencer_insight(self, request: InfluencerInsights) -> InfluencerDetail | GenericResponse:
        try:

            profile_visit_success = self.track_profile_visit(user_id=request.user_id,
                                                             influencer_id=request.influencer_id)

            if not profile_visit_success:
                return GenericResponse(success=False, button_text="REQUEST MORE COINS",
                                       message="Your coin balance is ZERO, please recharge to view more profiles")

            influencer = self.influencer_repository.get_influencer_by_id(influencer_id=request.influencer_id)
            influencer_metric = self.influencer_repository.get_latest_influencer_metric(
                influencer_id=request.influencer_id)

            collab_charge = InfluencerCollabCharge(
                min=influencer.content_charge,
                avg=(influencer_metric.insta_avg_views // 1000) * influencer.views_charge,
                max=(influencer_metric.insta_max_views // 1000) * influencer.views_charge,
            )
            instagram_detail = None
            if influencer.insta_username:
                instagram_detail = InstagramDetail(
                    username=influencer.insta_username,
                    followers=influencer_metric.insta_followers,
                    city_1=influencer_metric.insta_city_1,
                    city_pc_1=influencer_metric.insta_city_pc_1,
                    city_2=influencer_metric.insta_city_2,
                    city_pc_2=influencer_metric.insta_city_pc_2,
                    city_3=influencer_metric.insta_city_3,
                    city_pc_3=influencer_metric.insta_city_pc_3,
                    age_13_to_17=influencer_metric.insta_age_13_to_17,
                    age_18_to_24=influencer_metric.insta_age_18_to_24,
                    age_25_to_34=influencer_metric.insta_age_25_to_34,
                    age_35_to_44=influencer_metric.insta_age_35_to_44,
                    age_45_to_54=influencer_metric.insta_age_45_to_54,
                    age_55=influencer_metric.insta_age_55,
                    men_follower_pc=influencer_metric.insta_men_follower_pc,
                    women_follower_pc=influencer_metric.insta_women_follower_pc,
                    avg_views=influencer_metric.insta_avg_views,
                    max_views=influencer_metric.insta_max_views,
                    min_views=influencer_metric.insta_min_views,
                    spread=influencer_metric.insta_consistency_score,
                    avg_likes=influencer_metric.insta_avg_likes,
                    avg_comments=influencer_metric.insta_avg_comments,
                    avg_shares=influencer_metric.insta_avg_shares,
                    engagement_rate=influencer_metric.insta_engagement_rate
                )

            youtube_detail = None
            if influencer.yt_username:
                youtube_detail = YouTubeDetail(
                    username=influencer.yt_username,
                    followers=influencer_metric.yt_followers,
                    city_1=influencer_metric.yt_city_1,
                    city_pc_1=influencer_metric.yt_city_pc_1,
                    city_2=influencer_metric.yt_city_2,
                    city_pc_2=influencer_metric.yt_city_pc_2,
                    city_3=influencer_metric.yt_city_3,
                    city_pc_3=influencer_metric.yt_city_pc_3,
                    avg_views=influencer_metric.yt_avg_views,
                    max_views=influencer_metric.yt_max_views,
                    min_views=influencer_metric.yt_min_views,
                    spread=influencer_metric.yt_consistency_score,
                    avg_likes=influencer_metric.yt_avg_likes,
                    avg_comments=influencer_metric.yt_avg_comments,
                    avg_shares=influencer_metric.yt_avg_shares,
                    engagement_rate=influencer_metric.yt_engagement_rate
                )

            facebook_detail = None
            if influencer.fb_username:
                facebook_detail = FacebookDetail(
                    username=influencer.fb_username,
                    followers=influencer_metric.fb_followers,
                    city_1=influencer_metric.fb_city_1,
                    city_pc_1=influencer_metric.fb_city_pc_1,
                    city_2=influencer_metric.fb_city_2,
                    city_pc_2=influencer_metric.fb_city_pc_2,
                    city_3=influencer_metric.fb_city_3,
                    city_pc_3=influencer_metric.fb_city_pc_3,
                    avg_views=influencer_metric.fb_avg_views,
                    max_views=influencer_metric.fb_max_views,
                    min_views=influencer_metric.fb_min_views,
                    spread=influencer_metric.fb_consistency_score,
                    avg_likes=influencer_metric.fb_avg_likes,
                    avg_comments=influencer_metric.fb_avg_comments,
                    avg_shares=influencer_metric.fb_avg_shares,
                    engagement_rate=influencer_metric.fb_engagement_rate
                )

            platform_details = InfluencerMetricDetail(instagram_detail=instagram_detail,
                                                      youtube_detail=youtube_detail,
                                                      facebook_detail=facebook_detail)

            collaboration_request_raised = False
            all_collaboration_request_raised = self.campaign_repository.get_all_running_campaign_with_an_influencer(
                user_id=request.user_id, influencer_id=request.influencer_id)
            for request in all_collaboration_request_raised:
                if request.stage in [CampaignStage.CREATED, CampaignStage.INFLUENCER_FINALIZATION, CampaignStage.SHOOT,
                                     CampaignStage.POST, CampaignStage.FIRST_BILLING, CampaignStage.SECOND_BILLING]:
                    collaboration_request_raised = True
                    continue

            return InfluencerDetail(
                id=influencer.id,
                last_updated_at=influencer.last_updated_at,
                collaboration_request_raised=collaboration_request_raised,
                primary_platform=influencer.primary_platform,
                name=influencer.name,
                gender=influencer.gender,
                profile_picture=influencer.profile_picture,
                languages=influencer.languages,
                next_reach_score=0,
                niche=influencer.niche,
                city=influencer.city,
                collab_type=influencer.collab_type,
                deliverables=influencer.deliverables,
                content_charge=influencer.content_charge,
                views_charge=influencer.views_charge,
                collab_charge=collab_charge,
                platform_details=platform_details)

        except Exception as e:
            _log.error(
                f"Error occurred while fetching influencer details for influencer_id: {request.influencer_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="RETRY",
                                   message="Something went wrong while fetching influencer details")

    def create_lead(self, request: WaitListRequest) -> GenericResponse:
        wait_list = self.wait_list_user_repository.create_wait_list(request=request)

        if wait_list:
            return GenericResponse(success=True, message=None)
        else:
            return GenericResponse(success=False, message="Unable to create new wait_list")
