from typing import Optional, List

from app.database.waitlist_table import WaitList
from app.enums.average_view import AverageView
from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.engagement_rate import EngagementRate
from app.enums.follower_count import FollowerCount
from app.enums.gender import Gender
from app.enums.influencer_age import InfluencerAge
from app.enums.niche import Niche
from app.enums.platform import Platform
from app.enums.rating import Rating
from app.enums.reach_price import ReachPrice
from app.enums.status import Status
from app.repository.client_repository import ClientRepository
from app.repository.influencer_repository import InfluencerRepository
from app.repository.profile_visit_repository import ProfileVisitRepository
from app.repository.wait_list_repository import WaitListRepository
from app.requests.influencer_insights import InfluencerInsights
from app.requests.waitlist_request import WaitListRequest
from app.response.facebook_detail import FacebookDetail
from app.response.generic_response import GenericResponse
from app.response.influencer_collab_charge import InfluencerCollabCharge
from app.response.influencer_detail import InfluencerDetail
from app.response.influencer_listing import InfluencerListing
from app.response.influencer_metric_detail import InfluencerMetricDetail
from app.response.instagram_detail import InstagramDetail
from app.response.youtube_detail import YouTubeDetail
from app.utils.logger import configure_logger

_log = configure_logger()


class WebService:
    def __init__(self, session):
        self.influencer_repository = InfluencerRepository(session)
        self.wait_list_user_repository = WaitListRepository(session)
        self.profile_visit_repository = ProfileVisitRepository(session)
        self.client_repository = ClientRepository(session)

    def get_web_metadata(self) -> GenericResponse:
        pass

    def track_profile_visit(self, client_id: str, influencer_id: str) -> bool:
        """
        Track a profile visit. If the client has reached the maximum number of visits allowed,
        the visit is not logged, and an error is raised.
        """
        influencery_already_visited = self.profile_visit_repository.check_if_influencer_already_visited(client_id,
                                                                                                        influencer_id)
        if influencery_already_visited > 0:
            return True

        client = self.client_repository.get_client_by_id(client_id)
        balance_profile_visit_count = client.balance_profile_visits

        if balance_profile_visit_count > 0:
            # Log the profile visit in the database
            self.profile_visit_repository.log_profile_visit(client_id, influencer_id)
            self.client_repository.update_profile_visit_count(client_id)
            _log.info(f"Profile visit successfully logged for client {client_id} to influencer {influencer_id}.")
            return True
        else:
            _log.warning(
                f"Client {client_id} has no balance left to visit influencer {influencer_id}.")
            return False

    def get_influencer_listing(self, user_id: str,
                               page_number: int,
                               page_size: int,
                               niche: Optional[List[Niche]],
                               city: Optional[List[City]],
                               reach_price: Optional[List[ReachPrice]],
                               followers: Optional[List[FollowerCount]],
                               avg_views: Optional[List[AverageView]],
                               engagement: Optional[EngagementRate],
                               platform: Optional[Platform],
                               collab_type: Optional[CollabType],
                               gender: Optional[List[Gender]],
                               age: Optional[List[InfluencerAge]],
                               rating: Optional[Rating],
                               ) -> InfluencerListing:
        pass

    def get_influencer_insight(self, request: InfluencerInsights) -> InfluencerDetail | GenericResponse:
        try:
            influencer = self.influencer_repository.get_influencer_by_id(influencer_id=request.influencer_id)

            collab_charge = InfluencerCollabCharge(

                min=influencer.content_charge,
                average=influencer.views_charge * 100,
                max=influencer.content_charge * 1000,
            )
            instagram_detail = InstagramDetail()
            youtube_detail = YouTubeDetail()
            facebook_detail = FacebookDetail()

            platform_details = InfluencerMetricDetail(instagram_detail=instagram_detail, youtube_detail=youtube_detail,
                                                      facebook_detail=facebook_detail)

            return InfluencerDetail(
                id=influencer.id,
                last_updated_at=influencer.last_updated_at,
                collaboration_request_already_raised=False,
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
            return GenericResponse(success=False, button_text=None,
                                   message="Something went wrong while fetching influencer details")

    def create_lead(self, request: WaitListRequest) -> GenericResponse:
        wait_list = self.wait_list_user_repository.create_wait_list(request=request)

        if wait_list:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            return GenericResponse(success=False, button_text=None, message="Unable to create new wait_list")

    def update_lead(self, wait_list_id: str, status: Status) -> GenericResponse:
        wait_list = self.wait_list_user_repository.update_wait_list_status(wait_list_id=wait_list_id, status=status)

        if wait_list:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("No record found for wait_list with wait_list_id {}".format(wait_list_id))
            return GenericResponse(success=False, button_text=None,
                                   message="No wait_list found for given wait_list_id")

    def get_all_leads(self, page_size: int, page_number: int) -> List[WaitList] | GenericResponse:
        wait_list = self.wait_list_user_repository.get_wait_list(limit=page_size, offset=page_size * page_number)

        if wait_list and len(wait_list) > 0:
            return wait_list
        else:
            _log.info("No record found for wait_list page_size {}, page_number {}".format(page_size, page_number))
            return GenericResponse(success=False, button_text=None,
                                   message="No wait_list found for at all")
