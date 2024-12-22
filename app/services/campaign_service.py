from __future__ import print_function

from typing import List

from app.models.status import Status
from app.repository.campaign_repository import CampaignRepository
from app.repository.influencer_repository import InfluencerRepository
from app.requests.campaign_request import CampaignRequest
from app.requests.rate_campaign import RateCampaign
from app.response.campaign.billing_info import BillingInfo
from app.response.campaign.campaign_billing import CampaignBilling
from app.response.campaign.campaign_metrics import CampaignMetrics
from app.response.campaign.content_post import ContentPost
from app.response.campaign.influencer_basic_detail import InfluencerBasicDetail
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
                                                             influencer_basic_detail=InfluencerBasicDetail(
                                                                 influencer_id=campaign.influencer_id,
                                                                 influencer_image=influencer_basic_detail.profile_picture,
                                                                 niche=influencer_basic_detail.niche,
                                                                 city=influencer_basic_detail.city
                                                             ),
                                                             stage=campaign.stage,
                                                             status=campaign_stage_to_status(campaign.stage))
                campaign_basic_details.append(campaign_basic_detail)

            return campaign_basic_details

        except Exception as e:
            _log.error(f"Error occurred while fetching campaigns for client_id: {user_id}. Error: {str(e)}")
            return GenericResponse(success=False, error_code=None,
                                   error_message="Something went wrong while fetching your campaigns, please report the issue")

    def get_user_campaign_detail(self, campaign_id: str) -> CampaignDetail | GenericResponse:
        try:
            existing_campaign = self.campaign_repository.get_campaign_by_id(campaign_id)
            influencer = existing_campaign.influencer

            influencer_basic_detail = InfluencerBasicDetail(
                id=influencer.id,
                name=influencer.name,
                profile_picture=influencer.profile_picture,
                niche=influencer.niche,
                city=influencer.city,
                views_charge=influencer.views_charge,
                content_charge=influencer.content_charge
            )

            content_post = ContentPost(
                date=existing_campaign.content_post_date,
                insta_post_link=existing_campaign.insta_post_link,
                youtube_post_link=existing_campaign.youtube_post_link,
                fb_post_link=existing_campaign.fb_post_link,
                billing_info=BillingInfo(
                    billing_amount=existing_campaign.content_billing_amount,
                    billing_payment_at=existing_campaign.content_billing_payment_at,
                    billing_payment_status=existing_campaign.content_billing_payment_status
                )
            )
            first_billing = CampaignBilling(
                campaign_metrics=CampaignMetrics(
                    views=existing_campaign.first_billing_views,
                    likes=existing_campaign.first_billing_likes,
                    comments=existing_campaign.first_billing_comments,
                    shares=existing_campaign.first_billing_shares
                ),
                billing_info=BillingInfo(
                    billing_amount=existing_campaign.first_billing_amount,
                    billing_payment_at=existing_campaign.first_billing_payment_at,
                    billing_payment_status=existing_campaign.first_billing_payment_status
                )
            )
            second_billing = CampaignBilling(
                campaign_metrics=CampaignMetrics(
                    views=existing_campaign.second_billing_views,
                    likes=existing_campaign.second_billing_likes,
                    comments=existing_campaign.second_billing_comments,
                    shares=existing_campaign.second_billing_shares
                ),
                billing_info=BillingInfo(
                    billing_amount=existing_campaign.second_billing_amount,
                    billing_payment_at=existing_campaign.second_billing_payment_at,
                    billing_payment_status=existing_campaign.second_billing_payment_status
                )
            )

            return CampaignDetail(
                id=existing_campaign.id,
                last_updated_at=existing_campaign.last_updated_at,
                campaign_managed_by=existing_campaign.last_updated_at,
                influencer_basic_detail=influencer_basic_detail,
                stage=existing_campaign.stage,
                content_charge=existing_campaign.content_charge,
                views_charge=existing_campaign.views_charge,
                type_of_content=existing_campaign.type_of_content,
                campaign_notes=existing_campaign.campaign_notes,
                rating=existing_campaign.rating,
                review=existing_campaign.review,
                influencer_finalization_date=existing_campaign.influencer_finalization_date,
                content_shoot_date=existing_campaign.content_shoot_date,
                content_post=content_post,
                first_billing=first_billing,
                second_billing=second_billing,
                post_insights=existing_campaign.post_insights,
                pending_deliverables=existing_campaign.pending_deliverables
            )
        except Exception as e:
            _log.error(
                f"Error occurred while fetching campaigns details for campaign_id: {campaign_id}. Error: {str(e)}")
            return GenericResponse(success=False, error_code=None,
                                   error_message="Something went wrong while rating the campaign, campaign_id {}".format(
                                       campaign_id))

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
                    return GenericResponse(success=False, error_code=None,
                                           error_message="You can only rate the campaigns started by you")
                else:
                    return GenericResponse(success=True, error_code=None,
                                           error_message="Campaign rated successfully, campaign_id {}".format(
                                               request.campaign_id))

        except Exception as e:
            _log.error(
                f"Error occurred while rating campaign, campaign_id: {request.campaign_id}. Error: {str(e)}")
            return GenericResponse(success=False, error_code=None,
                                   error_message="Something went wrong while rating the campaign, campaign_id {}".format(
                                       request.campaign_id))

    def create_campaign(self, request: CampaignRequest) -> GenericResponse:
        timestamp_id = id_utils.get_campaign_id()
        try:
            db_campaign = self.campaign_repository.create_campaign(timestamp_id, request)
            return GenericResponse(success=True, error_code=None,
                                   error_message="Campaign created successfully, with campaign_id {}".format(
                                       db_campaign.id))
        except Exception as e:
            _log.error(
                f"Error occurred while fetching campaigns details for campaign_id: {timestamp_id}. Error: {str(e)}")
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
