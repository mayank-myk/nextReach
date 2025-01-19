from __future__ import print_function

from datetime import datetime, date
from io import BytesIO
from typing import List, Optional

import pandas as pd

from app.api_requests.campaign_completion_request import CampaignCompletionRequest
from app.api_requests.campaign_content_post_request import CampaignContentPostRequest
from app.api_requests.campaign_day2_billing_request import CampaignDay2BillingRequest
from app.api_requests.campaign_day8_billing_request import CampaignDay8BillingRequest
from app.api_requests.campaign_draft_approved_request import CampaignDraftApprovedRequest
from app.api_requests.campaign_influencer_finalized_request import CampaignInfluencerFinalizedRequest
from app.api_requests.campaign_pending_deliverables_request import CampaignPendingDeliverables
from app.api_requests.campaign_request import CampaignRequest
from app.api_requests.rate_campaign import RateCampaign
from app.api_requests.update_campaign_request import UpdateCampaignRequest
from app.enums.campaign_stage import CampaignStage
from app.repository.campaign_repository import CampaignRepository
from app.repository.influencer_repository import InfluencerRepository
from app.response.campaign.billing_info import BillingInfo
from app.response.campaign.campaign_billing import CampaignBilling
from app.response.campaign.campaign_metrics import CampaignMetrics
from app.response.campaign.content_draft import ContentDraft
from app.response.campaign.content_post import ContentPost
from app.response.campaign_basic_detail import CampaignBasicDetail
from app.response.campaign_detail import CampaignDetail
from app.response.campaign_detail_dump import CampaignDetailDump
from app.response.generic_response import GenericResponse
from app.response.influencer_basic_detail import InfluencerBasicDetail
from app.utils.converters import campaign_stage_to_status, int_to_str_k
from app.utils.logger import configure_logger

_log = configure_logger()


class CampaignService:
    def __init__(self, session):
        self.campaign_repository = CampaignRepository(session)
        self.influencer_repository = InfluencerRepository(session)

    def get_client_campaign_all(self, client_id: int) -> List[CampaignBasicDetail] | GenericResponse:
        try:
            all_campaigns = self.campaign_repository.get_all_campaign_by_client(client_id)
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
            _log.error(f"Error occurred while fetching campaigns for client_id: {client_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text="Try Again",
                                   message="Something went wrong while retrieving your campaigns")

    def get_client_campaign_detail(self, campaign_id: int) -> CampaignDetail | GenericResponse:
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

            content_draft = ContentDraft(
                date=existing_campaign.content_draft_date.strftime(
                    "%d %b %Y") if existing_campaign.content_post_date else None,
                billing_info=BillingInfo(
                    billing_amount=existing_campaign.content_billing_amount,
                    billing_payment_at=existing_campaign.content_billing_payment_at.strftime(
                        "%d %b %Y") if existing_campaign.content_billing_payment_at else None,
                    billing_payment_status=existing_campaign.content_billing_payment_status
                )
            )

            content_post = ContentPost(
                date=existing_campaign.content_post_date.strftime(
                    "%d %b %Y %I:%M %p") if existing_campaign.content_post_date else None,
                insta_post_link=existing_campaign.insta_post_link,
                yt_post_link=existing_campaign.yt_post_link,
                fb_post_link=existing_campaign.fb_post_link
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
                        "%d %b %Y") if existing_campaign.first_billing_payment_at else None,
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
                        "%d %b %Y") if existing_campaign.second_billing_payment_at else None,
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
            elif existing_campaign.stage == CampaignStage.INFLUENCER_FINALIZED:
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
            elif existing_campaign.stage == CampaignStage.SHOOT_COMPLETED:
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
            elif existing_campaign.stage == CampaignStage.DRAFT_APPROVED:
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
                    content_draft=content_draft,
                    pending_deliverables=existing_campaign.pending_deliverables
                )
            elif existing_campaign.stage == CampaignStage.CONTENT_POSTED:
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
                    content_draft=content_draft,
                    pending_deliverables=existing_campaign.pending_deliverables
                )
            elif existing_campaign.stage == CampaignStage.DAY2_BILLING:
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
                    content_draft=content_draft,
                    content_post=content_post,
                    first_billing=first_billing,
                    pending_deliverables=existing_campaign.pending_deliverables
                )
            elif existing_campaign.stage == CampaignStage.DAY8_BILLING:
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
                    content_draft=content_draft,
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
                    content_draft=content_draft,
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

    def get_all_active_campaign_detail(self) -> BytesIO:
        try:
            active_campaigns = self.campaign_repository.get_all_active_campaigns()
            campaign_detail_dump_list = []
            for campaign in active_campaigns:
                influencer = campaign.influencer
                client = campaign.client

                campaign_detail_dump = CampaignDetailDump(
                    campaign_id=campaign.id,
                    last_updated_at=campaign.last_updated_at.strftime(
                        "%d %b %Y %I:%M %p"),
                    campaign_notes=campaign.campaign_notes,
                    client_id=client.id,
                    client_phone_number=client.phone_number,
                    content_charge=campaign.content_charge,
                    views_charge=campaign.views_charge,
                    influencer_id=influencer.id,
                    influencer_name=influencer.name,
                    insta_username=influencer.influencer_insta_metric.user_name if influencer.influencer_insta_metric else None,
                    stage=campaign.stage.value,
                    ageing_day=(
                            datetime.today() - campaign.content_post_date).days if campaign.content_post_date else None,
                    influencer_finalization_date=campaign.influencer_finalization_date.strftime(
                        "%d %b %Y") if campaign.influencer_finalization_date else None,
                    content_shoot_date=campaign.content_shoot_date.strftime(
                        "%d %b %Y") if campaign.content_shoot_date else None,

                    content_draft_date=campaign.content_draft_date.strftime(
                        "%d %b %Y") if campaign.content_draft_date else None,
                    content_billing_amount=campaign.content_billing_amount,
                    content_billing_payment_at=campaign.content_billing_payment_at.strftime(
                        "%d %b %Y %I:%M %p") if campaign.content_billing_payment_at else None,
                    content_billing_payment_status=campaign.content_billing_payment_status.value if campaign.content_billing_payment_status else None,

                    content_post_date=campaign.content_post_date.strftime(
                        "%d %b %Y %I:%M %p") if campaign.content_post_date else None,
                    insta_post_link=campaign.insta_post_link,
                    yt_post_link=campaign.yt_post_link,
                    fb_post_link=campaign.fb_post_link,

                    first_billing_date=campaign.first_billing_date.strftime(
                        "%d %b %Y") if campaign.first_billing_date else None,
                    first_billing_views=campaign.first_billing_views,
                    first_billing_likes=campaign.first_billing_likes,
                    first_billing_comments=campaign.first_billing_comments,
                    first_billing_shares=campaign.first_billing_shares,
                    first_billing_amount=campaign.first_billing_amount,
                    first_billing_payment_at=campaign.first_billing_payment_at.strftime(
                        "%d %b %Y %I:%M %p") if campaign.first_billing_payment_at else None,
                    first_billing_payment_status=campaign.first_billing_payment_status.value if campaign.first_billing_payment_status else None,

                    second_billing_date=campaign.second_billing_date.strftime(
                        "%d %b %Y") if campaign.second_billing_date else None,
                    second_billing_views=campaign.second_billing_views,
                    second_billing_likes=campaign.second_billing_likes,
                    second_billing_comments=campaign.second_billing_comments,
                    second_billing_shares=campaign.second_billing_shares,
                    second_billing_amount=campaign.second_billing_amount,
                    second_billing_payment_at=campaign.second_billing_payment_at.strftime(
                        "%d %b %Y %I:%M %p") if campaign.second_billing_payment_at else None,
                    second_billing_payment_status=campaign.second_billing_payment_status.value if campaign.second_billing_payment_status else None,

                    post_insights=campaign.post_insights,
                    pending_deliverables=campaign.pending_deliverables
                )
                campaign_detail_dump_list.append(campaign_detail_dump)

            campaigns_data = [campaign.dict() for campaign in campaign_detail_dump_list]

            # Create a DataFrame from the list of dictionaries
            df = pd.DataFrame(campaigns_data)

            # Save the DataFrame to a BytesIO buffer
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name=f'Campaigns{datetime.today().strftime("%Y-%m-%d")}')
            buffer.seek(0)
            return buffer

        except Exception as e:
            _log.error(
                f"Error occurred while fetching campaigns details dump. Error: {str(e)}")

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
                elif existing_campaign.client_id != request.client_id:
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
            return GenericResponse(success=True, header="Success",
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
            return GenericResponse(success=True, header="Success",
                                   message="Campaign updated successfully, campaign_id {}".format(
                                       db_campaign.id))
        else:
            _log.info("No record found for campaign_id {}".format(campaign_id))
            return GenericResponse(success=False,
                                   message="No campaign found for given campaign_id")

    def update_campaign_to_influencer_finalization(self, campaign_id: int,
                                                   request: CampaignInfluencerFinalizedRequest) -> GenericResponse:
        db_campaign = self.campaign_repository.get_campaign_by_id(campaign_id=campaign_id)

        if db_campaign:
            if db_campaign.stage == CampaignStage.CREATED:
                updated_campaign = self.campaign_repository.update_campaign_to_influencer_finalization(
                    campaign_id=campaign_id, campaign_request=request)
                return GenericResponse(success=True, header="Success",
                                       message="Campaign updated successfully, campaign_id {}".format(
                                           updated_campaign.id))
            else:
                return GenericResponse(success=False, header="Failed",
                                       message="Campaign with campaign_id: {} is already in state: {}, you can only update from CREATED to INFLUENCER_FINALIZED".format(
                                           db_campaign.id, db_campaign.stage))
        else:
            return GenericResponse(success=False, button_text="Check again",
                                   message="No campaign found for given campaign_id")

    def update_campaign_to_shoot_completed(self, campaign_id: int, content_shoot_date: date) -> GenericResponse:
        db_campaign = self.campaign_repository.get_campaign_by_id(campaign_id=campaign_id)

        if db_campaign:
            if db_campaign.stage == CampaignStage.INFLUENCER_FINALIZED:
                updated_campaign = self.campaign_repository.update_campaign_to_shoot_completed(
                    campaign_id=campaign_id, content_shoot_date=content_shoot_date)
                return GenericResponse(success=True, header="Success",
                                       message="Campaign updated successfully, campaign_id {}".format(
                                           updated_campaign.id))
            else:
                return GenericResponse(success=False, header="Failed",
                                       message="Campaign with campaign_id: {} is already in state: {}, you can only update from INFLUENCER_FINALIZED to SHOOT_COMPLETED".format(
                                           db_campaign.id, db_campaign.stage))
        else:
            return GenericResponse(success=False, button_text="Check again",
                                   message="No campaign found for given campaign_id")

    def update_campaign_to_draft_approved(self, campaign_id: int,
                                          request: CampaignDraftApprovedRequest) -> GenericResponse:
        db_campaign = self.campaign_repository.get_campaign_by_id(campaign_id=campaign_id)

        if db_campaign:
            if db_campaign.stage == CampaignStage.SHOOT_COMPLETED:
                updated_campaign = self.campaign_repository.update_campaign_to_draft_approved(
                    campaign_id=campaign_id, campaign_request=request)
                return GenericResponse(success=True, header="Success",
                                       message="Campaign updated successfully, campaign_id {}".format(
                                           updated_campaign.id))
            else:
                return GenericResponse(success=False, header="Failed",
                                       message="Campaign with campaign_id: {} is already in state: {}, you can only update from SHOOT_COMPLETED to DRAFT_APPROVED".format(
                                           db_campaign.id, db_campaign.stage))
        else:
            return GenericResponse(success=False, button_text="Check again",
                                   message="No campaign found for given campaign_id")

    def update_campaign_to_content_posted(self, campaign_id: int,
                                          request: CampaignContentPostRequest) -> GenericResponse:
        db_campaign = self.campaign_repository.get_campaign_by_id(campaign_id=campaign_id)

        if db_campaign:
            if db_campaign.stage == CampaignStage.DRAFT_APPROVED:
                updated_campaign = self.campaign_repository.update_campaign_to_content_posted(
                    campaign_id=campaign_id, campaign_request=request)
                return GenericResponse(success=True, header="Success",
                                       message="Campaign updated successfully, campaign_id {}".format(
                                           updated_campaign.id))
            else:
                return GenericResponse(success=False, header="Failed",
                                       message="Campaign with campaign_id: {} is already in state: {}, you can only update from DRAFT_APPROVED to CONTENT_POSTED".format(
                                           db_campaign.id, db_campaign.stage))
        else:
            return GenericResponse(success=False, button_text="Check again",
                                   message="No campaign found for given campaign_id")

    def update_campaign_to_day2_billing(self, campaign_id: int, request: CampaignDay2BillingRequest) -> GenericResponse:
        db_campaign = self.campaign_repository.get_campaign_by_id(campaign_id=campaign_id)

        if db_campaign:
            if db_campaign.stage == CampaignStage.CONTENT_POSTED:
                updated_campaign = self.campaign_repository.update_campaign_to_day2_billing(
                    campaign_id=campaign_id, campaign_request=request)
                return GenericResponse(success=True, header="Success",
                                       message="Campaign updated successfully, campaign_id {}".format(
                                           updated_campaign.id))
            else:
                return GenericResponse(success=False, header="Failed",
                                       message="Campaign with campaign_id: {} is already in state: {}, you can only update from CONTENT_POSTED to DAY2_BILLING".format(
                                           db_campaign.id, db_campaign.stage))
        else:
            return GenericResponse(success=False, button_text="Check again",
                                   message="No campaign found for given campaign_id")

    def update_campaign_to_day8_billing(self, campaign_id: int, request: CampaignDay8BillingRequest) -> GenericResponse:
        db_campaign = self.campaign_repository.get_campaign_by_id(campaign_id=campaign_id)

        if db_campaign:
            if db_campaign.stage == CampaignStage.DAY2_BILLING:
                updated_campaign = self.campaign_repository.update_campaign_to_day8_billing(
                    campaign_id=campaign_id, campaign_request=request)
                return GenericResponse(success=True, header="Success",
                                       message="Campaign updated successfully, campaign_id {}".format(
                                           updated_campaign.id))
            else:
                return GenericResponse(success=False, header="Failed",
                                       message="Campaign with campaign_id: {} is already in state: {}, you can only update from DAY2_BILLING to DAY8_BILLING".format(
                                           db_campaign.id, db_campaign.stage))
        else:
            return GenericResponse(success=False, button_text="Check again",
                                   message="No campaign found for given campaign_id")

    def update_campaign_to_completed(self, campaign_id: int,
                                     request: Optional[CampaignCompletionRequest]) -> GenericResponse:
        db_campaign = self.campaign_repository.get_campaign_by_id(campaign_id=campaign_id)

        if db_campaign:
            if db_campaign.stage == CampaignStage.DAY8_BILLING:
                if request:
                    post_insights = [
                        value for key, value in request.dict().items() if value is not None
                    ]
                    updated_campaign = self.campaign_repository.update_campaign_to_completed(campaign_id=campaign_id,
                                                                                             post_insights=post_insights)
                else:
                    updated_campaign = self.campaign_repository.update_campaign_to_completed(campaign_id=campaign_id,
                                                                                             post_insights=None)

                return GenericResponse(success=True, header="Success",
                                       message="Campaign updated successfully, campaign_id {}".format(
                                           updated_campaign.id))
            else:
                return GenericResponse(success=False, header="Failed",
                                       message="Campaign with campaign_id: {} is already in state: {}, you can only update from DAY8_BILLING to COMPLETED".format(
                                           db_campaign.id, db_campaign.stage))
        else:
            return GenericResponse(success=False, button_text="Check again",
                                   message="No campaign found for given campaign_id")

    def update_campaign_to_cancelled(self, campaign_id: int) -> GenericResponse:
        db_campaign = self.campaign_repository.get_campaign_by_id(campaign_id=campaign_id)

        if db_campaign:
            updated_campaign = self.campaign_repository.update_campaign_to_cancelled(campaign_id=campaign_id)
            return GenericResponse(success=True, header="Success",
                                   message="Campaign updated successfully, campaign_id {}".format(
                                       updated_campaign.id))

        else:
            return GenericResponse(success=False, button_text="Check again",
                                   message="No campaign found for given campaign_id")

    def update_campaign_pending_deliverables(self, campaign_id: int,
                                             request: CampaignPendingDeliverables) -> GenericResponse:
        db_campaign = self.campaign_repository.get_campaign_by_id(campaign_id=campaign_id)

        if db_campaign:
            pending_deliverables = [
                value for key, value in request.dict().items() if value is not None
            ]
            updated_campaign = self.campaign_repository.update_campaign_pending_deliverables(campaign_id=campaign_id,
                                                                                             pending_deliverables=pending_deliverables)
            return GenericResponse(success=True, header="Success",
                                   message="Campaign updated successfully, campaign_id {}".format(
                                       updated_campaign.id))

        else:
            return GenericResponse(success=False, button_text="Check again",
                                   message="No campaign found for given campaign_id")
