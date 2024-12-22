from __future__ import print_function

from typing import List

from app.models.status import Status
from app.repository.campaign_repository import CampaignRepository
from app.repository.influencer_repository import InfluencerRepository
from app.requests.campaign_request import CampaignRequest
from app.requests.rate_campaign import RateCampaign
from app.response.campaign_basic_details import CampaignBasicDetails
from app.response.campaign_detail import CampaignDetail
from app.response.generic_response import GenericResponse
from app.utils import id_utils
from app.utils.converters import campaign_stage_to_status
from app.utils.logger import configure_logger

_log = configure_logger()


class CampaignService:
    def __init__(self, session):
        self.campaign_repository = CampaignRepository(session)
        self.influencer_repository = InfluencerRepository(session)

    def get_user_campaign_all(self, user_id: str) -> List[CampaignBasicDetails] | GenericResponse:
        try:
            all_campaigns = self.campaign_repository.get_all_campaign_for_a_user(user_id)
            campaign_basic_details = []
            for campaign in all_campaigns:
                influencer_basic_detail = self.influencer_repository.get_influencer_by_id(
                    influencer_id=campaign.influencer_id)
                campaign_basic_detail = CampaignBasicDetails(id=campaign.id,
                                                             created_at=campaign.created_at,
                                                             influencer_id=campaign.influencer_id,
                                                             influencer_image=influencer_basic_detail.profile_picture,
                                                             niche=influencer_basic_detail.niche,
                                                             city=influencer_basic_detail.city,
                                                             stage=campaign.stage,
                                                             status=campaign_stage_to_status(campaign.stage))
                campaign_basic_details.append(campaign_basic_detail)

            return campaign_basic_details

        except Exception as e:
            _log.error(f"Error occurred while fetching campaigns for client_id: {user_id}. Error: {str(e)}")
            return GenericResponse(success=False, error_code=None,
                                   error_message="Something went wrong while fetching your campaigns, please report the issue")

    def get_user_campaign_detail(self, campaign_id: str) -> CampaignDetail:
        try:
            return self.campaign_repository.get_campaign_by_id(campaign_id)
        except Exception as e:
            raise Exception

    def rate_campaign(self, request: RateCampaign) -> GenericResponse:
        try:
            existing_campaign = self.campaign_repository.create_campaign_rating(request)

            if not existing_campaign:
                return GenericResponse(success=False, error_code=None,
                                       error_message="No Campaign found for campaign_id {}".format(request.campaign_id))
            else:
                if existing_campaign.status != Status.COMPLETED:
                    return GenericResponse(success=False, error_code=None,
                                           error_message="You can only rate once campaign is completed")
                elif existing_campaign.client.id != request.user_id:
                    raise ValueError(f"Given client has not started this campaign")
                else:
                    return GenericResponse(success=True, error_code=None,
                                           error_message="Campaign rated successfully, campaign_id {}".format(
                                               request.campaign_id))

        except Exception as e:
            return GenericResponse(success=False, error_code=None,
                                   error_message="Something went wrong while rating the campaign, campaign_id {}".format(
                                       request.campaign_id))

    def create_campaign(self, request: CampaignRequest) -> GenericResponse:
        try:
            timestamp_id = id_utils.get_campaign_id()
            db_campaign = self.campaign_repository.create_campaign(timestamp_id, request)
            return GenericResponse(success=True, error_code=None,
                                   error_message="Campaign created successfully, with campaign_id {}".format(db_campaign.id))
        except Exception as e:
            return GenericResponse(success=False, error_code=None,
                                   error_message="Campaign creation failed")

    def update_campaign(self, campaign_id: str, request: CampaignRequest) -> GenericResponse:
        db_campaign = self.campaign_repository.update_campaign(campaign_id, request)

        if db_campaign:
            return GenericResponse(success=True, error_code=None,
                                   error_message="Campaign updated successfully, campaign_id {}".format(
                                       db_campaign.id))
        else:
            _log.info("No record found for campaign_id {}".format(campaign_id))
            return GenericResponse(success=False, error_code=None,
                                   error_message="No campaign found for given campaign_id")
