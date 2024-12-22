from __future__ import print_function

from typing import List
from app.response.campaign_detail import CampaignDetail
from app.repository.campaign_repository import CampaignRepository
from app.requests.campaign_request import CampaignRequest
from app.response.campaign_basic_details import CampaignBasicDetails
from app.response.generic_response import GenericResponse
from app.requests.rate_campaign import RateCampaign
from app.utils import id_utils
from app.utils.logger import configure_logger

_log = configure_logger()


class CampaignService:
    def __init__(self, session):
        self.campaign_repository = CampaignRepository(session)

    def get_user_campaign_all(self, user_id: str) -> List[CampaignBasicDetails]:
        try:
            return self.campaign_repository.get_all_campaign_for_a_user(user_id)
        except Exception as e:
            raise Exception

    def get_user_campaign_detail(self, campaign_id: str) -> CampaignDetail:
        try:
            return self.campaign_repository.get_campaign_by_id(campaign_id)
        except Exception as e:
            raise Exception

    def rate_campaign(self, request: RateCampaign) -> GenericResponse:
        try:
            db_campaign = self.campaign_repository.create_campaign_rating(request)
            return GenericResponse(success=True, error_code=None,
                                   error_message="Campaign rated successfully, campaign_id {}".format(db_campaign.id))
        except Exception as e:
            return GenericResponse(success=False, error_code=None,
                                   error_message="Campaign rate giving failed")

    def create_campaign(self, request: CampaignRequest) -> GenericResponse:
        try:
            timestamp_id = id_utils.get_campaign_id()
            db_campaign = self.campaign_repository.create_campaign(timestamp_id, request)
            return GenericResponse(success=True, error_code=None,
                                   error_message="Campaign created successfully, campaign_id {}".format(db_campaign.id))
        except Exception as e:
            return GenericResponse(success=False, error_code=None,
                                   error_message="Campaign creation failed")

    def update_campaign(self, campaign_id: str, request: CampaignRequest) -> GenericResponse:
        try:
            db_campaign = self.campaign_repository.update_campaign(campaign_id, request)
            return GenericResponse(success=True, error_code=None,
                                   error_message="Campaign updated successfully, campaign_id {}".format(db_campaign.id))
        except Exception as e:
            return GenericResponse(success=False, error_code=None,
                                   error_message="Campaign updation failed")
