from typing import Optional, List
from app.models.city import City
from app.models.gender import Gender
from app.models.niche import Niche
from app.models.platform import Platform
from app.models.status import Status
from app.repository.client_repository import ClientRepository
from app.repository.influencer_repository import InfluencerRepository
from app.repository.profile_visit_repository import ProfileVisitRepository
from app.repository.wait_list_repository import WaitListRepository
from app.requests.waitlist_request import WaitListRequest
from app.response.generic_response import GenericResponse
from app.requests.influencer_insights import InfluencerInsights
from app.response.influencer_detail import InfluencerDetail
from app.response.influencer_listing import InfluencerListing
from app.utils.logger import configure_logger
from datetime import datetime

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
                               platform: Optional[Platform],
                               content_price: Optional[List[int]],
                               reach_price: Optional[List[int]],
                               niche: Optional[List[Niche]],
                               gender: Optional[List[Gender]],
                               age: Optional[List[int]],
                               city: Optional[List[City]],
                               rating: Optional[int],
                               followers: Optional[List[int]],
                               avg_views: Optional[List[int]],
                               engagement: Optional[int],
                               consistency: Optional[int],
                               score: Optional[int]) -> InfluencerListing:
        # Generate a timestamp-based ID
        timestamp_id = 'B' + datetime.now().strftime('%Y%m%d%H%M%S')
        pass

    def get_influencer_insight(self, request: InfluencerInsights) -> InfluencerDetail:
        pass

    def create_lead(self, request: WaitListRequest) -> GenericResponse:
        wait_list = self.wait_list_user_repository.create_wait_list(request=request)

        if wait_list:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None, error_message="Unable to create new wait_list")

    def update_lead(self, wait_list_id: str, status: Status) -> GenericResponse:
        wait_list = self.wait_list_user_repository.update_wait_list_status(wait_list_id=wait_list_id, status=status)

        if wait_list:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None,
                                   error_message="No wait_list found for given wait_list_id")

    def get_all_leads(self, page_size: int, page_number: int) -> GenericResponse:
        wait_list = self.wait_list_user_repository.get_wait_list(limit=page_size, offset=page_size * page_number)

        if wait_list:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None,
                                   error_message="No wait_list found for at all")
