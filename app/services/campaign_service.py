from __future__ import print_function

from typing import List

from app.api_requests.campaign_request import CampaignRequest
from app.api_requests.rate_campaign import RateCampaign
from app.api_requests.update_campaign_request import UpdateCampaignRequest
from app.enums.campaign_stage import CampaignStage
from app.repository.campaign_repository import CampaignRepository
from app.repository.influencer_repository import InfluencerRepository
from app.response.campaign.billing_info import BillingInfo
from app.response.campaign.campaign_billing import CampaignBilling
from app.response.campaign.campaign_metrics import CampaignMetrics
from app.response.campaign.content_post import ContentPost
from app.response.campaign_basic_detail import CampaignBasicDetail
from app.response.campaign_detail import CampaignDetail
from app.response.generic_response import GenericResponse
from app.response.influencer_basic_detail import InfluencerBasicDetail
from app.utils.converters import campaign_stage_to_status, int_to_str_k
from app.utils.logger import configure_logger

_log = configure_logger()


class CampaignService:
    def __init__(self, session):
        self.campaign_repository = CampaignRepository(session)
        self.influencer_repository = InfluencerRepository(session)

    def get_user_campaign_all(self, user_id: int) -> List[CampaignBasicDetail] | GenericResponse:
        try:
            all_campaigns = self.campaign_repository.get_all_campaign_by_an_user(user_id)
            campaign_basic_details = []
            for campaign in all_campaigns:
                influencer_basic_detail = self.influencer_repository.get_influencer_by_id(
                    influencer_id=campaign.influencer_id)
                campaign_basic_detail = CampaignBasicDetail(id=campaign.id,
                                                            last_updated_at=campaign.last_updated_at.strftime(
                                                                "%d %b %Y"),
                                                            influencer_basic_detail=InfluencerBasicDetail(
                                                                id=campaign.influencer_id,
                                                                name=influencer_basic_detail.name,
                                                                profile_picture=influencer_basic_detail.profile_picture,
                                                                niche=influencer_basic_detail.niche,
                                                                city=influencer_basic_detail.city,
                                                                profile_visited=True
                                                            ),
                                                            status=campaign_stage_to_status(campaign.stage))
                campaign_basic_details.append(campaign_basic_detail)

            return campaign_basic_details

        except Exception as e:
            _log.error(f"Error occurred while fetching campaigns for user_id: {user_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Try Again",
                                   message="Something went wrong while retrieving your campaigns")

    def get_user_campaign_detail(self, campaign_id: int) -> CampaignDetail | GenericResponse:
        try:
            existing_campaign = self.campaign_repository.get_campaign_by_id(campaign_id)
            if not existing_campaign:
                return GenericResponse(success=False, button_text="Understood",
                                       message="No campaign details found")

            influencer = existing_campaign.influencer

            influencer_basic_detail = InfluencerBasicDetail(
                id=influencer.id,
                name=influencer.name,
                profile_picture=influencer.profile_picture,
                niche=influencer.niche,
                city=influencer.city,
                views_charge=existing_campaign.views_charge,
                content_charge=existing_campaign.content_charge,
                profile_visited=True
            )

            influencer_finalization_date = existing_campaign.influencer_finalization_date.strftime(
                "%d %b %Y") if existing_campaign.influencer_finalization_date else None
            content_shoot_date = existing_campaign.content_shoot_date.strftime(
                "%d %b %Y") if existing_campaign.content_shoot_date else None

            content_post = ContentPost(
                date=existing_campaign.content_post_date.strftime(
                    "%d %b %Y") if existing_campaign.content_post_date else None,
                insta_post_link=existing_campaign.insta_post_link,
                youtube_post_link=existing_campaign.youtube_post_link,
                fb_post_link=existing_campaign.fb_post_link,
                billing_info=BillingInfo(
                    billing_amount=existing_campaign.content_billing_amount,
                    billing_payment_at=existing_campaign.content_billing_payment_at.strftime(
                        "%d %b %Y %I:%M %p") if existing_campaign.content_billing_payment_at else None,
                    billing_payment_status=existing_campaign.content_billing_payment_status
                )
            )

            first_billing = CampaignBilling(
                date=existing_campaign.first_billing_date.strftime(
                    "%d %b %Y") if existing_campaign.first_billing_date else None,
                campaign_metrics=CampaignMetrics(
                    views=int_to_str_k(existing_campaign.first_billing_views),
                    likes=int_to_str_k(existing_campaign.first_billing_likes),
                    comments=int_to_str_k(existing_campaign.first_billing_comments),
                    shares=int_to_str_k(existing_campaign.first_billing_shares)
                ),
                billing_info=BillingInfo(
                    billing_amount=existing_campaign.first_billing_amount,
                    billing_payment_at=existing_campaign.first_billing_payment_at.strftime(
                        "%d %b %Y %I:%M %p") if existing_campaign.first_billing_payment_at else None,
                    billing_payment_status=existing_campaign.first_billing_payment_status
                )
            )

            second_billing = CampaignBilling(
                date=existing_campaign.second_billing_date.strftime(
                    "%d %b %Y") if existing_campaign.second_billing_date else None,
                campaign_metrics=CampaignMetrics(
                    views=int_to_str_k(existing_campaign.second_billing_views),
                    likes=int_to_str_k(existing_campaign.second_billing_likes),
                    comments=int_to_str_k(existing_campaign.second_billing_comments),
                    shares=int_to_str_k(existing_campaign.second_billing_shares)
                ),
                billing_info=BillingInfo(
                    billing_amount=existing_campaign.second_billing_amount,
                    billing_payment_at=existing_campaign.second_billing_payment_at.strftime(
                        "%d %b %Y %I:%M %p") if existing_campaign.second_billing_payment_at else None,
                    billing_payment_status=existing_campaign.second_billing_payment_status
                )
            )
            if existing_campaign.stage == CampaignStage.CREATED:
                return CampaignDetail(
                    id=existing_campaign.id,
                    last_updated_at=existing_campaign.last_updated_at,
                    campaign_managed_by=existing_campaign.campaign_managed_by,
                    influencer_basic_detail=influencer_basic_detail,
                    stage=existing_campaign.stage,
                    type_of_content=existing_campaign.type_of_content,
                    campaign_notes=existing_campaign.campaign_notes,
                    pending_deliverables=existing_campaign.pending_deliverables
                )
            elif existing_campaign.stage == CampaignStage.INFLUENCER_FINALIZATION:
                return CampaignDetail(
                    id=existing_campaign.id,
                    last_updated_at=existing_campaign.last_updated_at,
                    campaign_managed_by=existing_campaign.campaign_managed_by,
                    influencer_basic_detail=influencer_basic_detail,
                    stage=existing_campaign.stage,
                    type_of_content=existing_campaign.type_of_content,
                    campaign_notes=existing_campaign.campaign_notes,
                    influencer_finalization_date=influencer_finalization_date,
                    pending_deliverables=existing_campaign.pending_deliverables
                )
            elif existing_campaign.stage == CampaignStage.SHOOT:
                return CampaignDetail(
                    id=existing_campaign.id,
                    last_updated_at=existing_campaign.last_updated_at,
                    campaign_managed_by=existing_campaign.campaign_managed_by,
                    influencer_basic_detail=influencer_basic_detail,
                    stage=existing_campaign.stage,
                    type_of_content=existing_campaign.type_of_content,
                    campaign_notes=existing_campaign.campaign_notes,
                    influencer_finalization_date=influencer_finalization_date,
                    content_shoot_date=content_shoot_date,
                    pending_deliverables=existing_campaign.pending_deliverables
                )
            elif existing_campaign.stage == CampaignStage.POST:
                return CampaignDetail(
                    id=existing_campaign.id,
                    last_updated_at=existing_campaign.last_updated_at,
                    campaign_managed_by=existing_campaign.campaign_managed_by,
                    influencer_basic_detail=influencer_basic_detail,
                    stage=existing_campaign.stage,
                    type_of_content=existing_campaign.type_of_content,
                    campaign_notes=existing_campaign.campaign_notes,
                    influencer_finalization_date=influencer_finalization_date,
                    content_shoot_date=content_shoot_date,
                    content_post=content_post,
                    pending_deliverables=existing_campaign.pending_deliverables
                )
            elif existing_campaign.stage == CampaignStage.FIRST_BILLING:
                return CampaignDetail(
                    id=existing_campaign.id,
                    last_updated_at=existing_campaign.last_updated_at,
                    campaign_managed_by=existing_campaign.campaign_managed_by,
                    influencer_basic_detail=influencer_basic_detail,
                    stage=existing_campaign.stage,
                    type_of_content=existing_campaign.type_of_content,
                    campaign_notes=existing_campaign.campaign_notes,
                    influencer_finalization_date=influencer_finalization_date,
                    content_shoot_date=content_shoot_date,
                    content_post=content_post,
                    first_billing=first_billing,
                    pending_deliverables=existing_campaign.pending_deliverables
                )
            elif existing_campaign.stage == CampaignStage.SECOND_BILLING:
                return CampaignDetail(
                    id=existing_campaign.id,
                    last_updated_at=existing_campaign.last_updated_at,
                    campaign_managed_by=existing_campaign.campaign_managed_by,
                    influencer_basic_detail=influencer_basic_detail,
                    stage=existing_campaign.stage,
                    type_of_content=existing_campaign.type_of_content,
                    campaign_notes=existing_campaign.campaign_notes,
                    influencer_finalization_date=influencer_finalization_date,
                    content_shoot_date=content_shoot_date,
                    content_post=content_post,
                    first_billing=first_billing,
                    second_billing=second_billing,
                    pending_deliverables=existing_campaign.pending_deliverables,
                    post_insights=existing_campaign.post_insights
                )
            elif existing_campaign.stage == CampaignStage.COMPLETED:
                return CampaignDetail(
                    id=existing_campaign.id,
                    last_updated_at=existing_campaign.last_updated_at,
                    campaign_managed_by=existing_campaign.campaign_managed_by,
                    influencer_basic_detail=influencer_basic_detail,
                    stage=existing_campaign.stage,
                    type_of_content=existing_campaign.type_of_content,
                    campaign_notes=existing_campaign.campaign_notes,
                    influencer_finalization_date=influencer_finalization_date,
                    content_shoot_date=content_shoot_date,
                    content_post=content_post,
                    first_billing=first_billing,
                    second_billing=second_billing,
                    pending_deliverables=existing_campaign.pending_deliverables,
                    post_insights=existing_campaign.post_insights,
                    rating=existing_campaign.rating,
                    review=existing_campaign.review,
                )
            else:
                return CampaignDetail(
                    id=existing_campaign.id,
                    last_updated_at=existing_campaign.last_updated_at,
                    campaign_managed_by=existing_campaign.campaign_managed_by,
                    influencer_basic_detail=influencer_basic_detail,
                    stage=existing_campaign.stage,
                    type_of_content=existing_campaign.type_of_content,
                    campaign_notes=existing_campaign.campaign_notes
                )
        except Exception as e:
            _log.error(
                f"Error occurred while fetching campaigns details for campaign_id: {campaign_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Try Again",
                                   message="Something went wrong while retrieving campaign details")

    def rate_campaign(self, request: RateCampaign) -> GenericResponse:
        try:
            existing_campaign = self.campaign_repository.create_campaign_rating(request)

            if not existing_campaign:
                return GenericResponse(success=False, button_text="Understood",
                                       message="No campaign found with the provided details")
            else:
                if existing_campaign.stage != CampaignStage.COMPLETED:
                    return GenericResponse(success=False, button_text="Understood",
                                           message="You can only submit a rating once the campaign has been completed")
                elif existing_campaign.user_id != request.user_id:
                    return GenericResponse(success=False, button_text="Understood",
                                           message="You can only rate campaigns that you have initiated")
                else:
                    return GenericResponse(success=True, header="Thanks!", button_text="Go Back",
                                           message="Your feedback helps us improve the platform and provide better experiences for all users.")

        except Exception as e:
            _log.error(
                f"Error occurred while rating campaign, campaign_id: {request.campaign_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Retry",
                                   message="Something went wrong while rating the campaign")

    def create_campaign(self, request: CampaignRequest) -> GenericResponse:
        try:
            db_campaign = self.campaign_repository.create_campaign(request)
            return GenericResponse(success=True,
                                   message="Campaign created successfully, with campaign_id {}".format(
                                       db_campaign.id))
        except Exception as e:
            _log.error(
                f"Error occurred while creating campaign. Error: {str(e)}")
            return GenericResponse(success=False,
                                   message="Campaign creation failed")

    def update_campaign(self, campaign_id: int, request: UpdateCampaignRequest) -> GenericResponse:
        db_campaign = self.campaign_repository.update_campaign(campaign_id, request)

        if db_campaign:
            return GenericResponse(success=True,
                                   message="Campaign updated successfully, campaign_id {}".format(
                                       db_campaign.id))
        else:
            _log.info("No record found for campaign_id {}".format(campaign_id))
            return GenericResponse(success=False,
                                   message="No campaign found for given campaign_id")
