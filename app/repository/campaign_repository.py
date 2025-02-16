from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from app.api_requests.campaign_content_post_request import CampaignContentPostRequest
from app.api_requests.campaign_day2_billing_request import CampaignDay2BillingRequest
from app.api_requests.campaign_day2_payment_request import CampaignDay2PaymentRequest
from app.api_requests.campaign_day8_billing_request import CampaignDay8BillingRequest
from app.api_requests.campaign_day8_payment_request import CampaignDay8PaymentRequest
from app.api_requests.campaign_influencer_finalized_request import CampaignInfluencerFinalizedRequest
from app.api_requests.campaign_request import CampaignRequest
from app.api_requests.rate_campaign import RateCampaign
from app.api_requests.update_campaign_request import UpdateCampaignRequest
from app.database.campaign_table import Campaign
from app.database.influencer_table import Influencer
from app.enums.campaign_stage import CampaignStage
from app.enums.collab_date import CollabDate, COLLAB_DATE_DICT
from app.enums.payment_status import PaymentStatus
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class CampaignRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_campaign(self, campaign_request: CampaignRequest) -> Campaign:
        new_campaign = Campaign(
            created_by=campaign_request.created_by,
            last_updated_by=campaign_request.created_by,
            campaign_managed_by=campaign_request.campaign_managed_by,
            influencer_id=campaign_request.influencer_id,
            client_id=campaign_request.client_id,
            stage=CampaignStage.CREATED,
            content_charge=campaign_request.content_charge,
            views_charge=campaign_request.views_charge,
            type_of_content=campaign_request.type_of_content,
            campaign_notes=campaign_request.campaign_notes,
            rating=campaign_request.rating,
            review=campaign_request.review,
            influencer_finalization_date=campaign_request.influencer_finalization_date,
            content_shoot_date=campaign_request.content_shoot_date,
            content_post_date=campaign_request.content_post_date,
            insta_post_link=campaign_request.insta_post_link,
            yt_post_link=campaign_request.yt_post_link,
            fb_post_link=campaign_request.fb_post_link,
            content_billing_amount=campaign_request.content_billing_amount,
            content_billing_payment_at=campaign_request.content_billing_payment_at,
            content_billing_payment_status=campaign_request.content_billing_payment_status,
            first_billing_date=campaign_request.first_billing_date,
            first_billing_views=campaign_request.first_billing_views,
            first_billing_likes=campaign_request.first_billing_likes,
            first_billing_comments=campaign_request.first_billing_comments,
            first_billing_shares=campaign_request.first_billing_shares,
            first_billing_amount=campaign_request.first_billing_amount,
            first_billing_payment_at=campaign_request.first_billing_payment_at,
            first_billing_payment_status=campaign_request.first_billing_payment_status,
            second_billing_date=campaign_request.first_billing_date,
            second_billing_views=campaign_request.second_billing_views,
            second_billing_likes=campaign_request.second_billing_likes,
            second_billing_comments=campaign_request.second_billing_comments,
            second_billing_shares=campaign_request.second_billing_shares,
            second_billing_amount=campaign_request.second_billing_amount,
            second_billing_payment_at=campaign_request.second_billing_payment_at,
            second_billing_payment_status=campaign_request.second_billing_payment_status,
            post_insights=campaign_request.post_insights,
            pending_deliverables=campaign_request.pending_deliverables
        )

        self.db.add(new_campaign)
        self.db.commit()
        self.db.refresh(new_campaign)
        return new_campaign

    def create_collab_campaign(self, created_by: str, client_id: int, influencer: Influencer,
                               collab_date: Optional[CollabDate]) -> Campaign:

        new_campaign = Campaign(
            created_by=created_by,
            last_updated_by=created_by,
            campaign_managed_by=created_by,
            influencer_id=influencer.id,
            content_charge=influencer.content_charge,
            views_charge=influencer.views_charge,
            client_id=client_id,
            stage=CampaignStage.CREATED,
            campaign_notes=COLLAB_DATE_DICT[collab_date] if collab_date else None
        )

        self.db.add(new_campaign)
        self.db.commit()
        self.db.refresh(new_campaign)
        return new_campaign

    def update_campaign(self, campaign_id: int, campaign_request: UpdateCampaignRequest) -> Optional[Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)

            if not existing_campaign:
                return None

            if hasattr(campaign_request, 'updated_by') and campaign_request.updated_by is not None:
                setattr(existing_campaign, 'last_updated_by', campaign_request.updated_by)

            if hasattr(campaign_request, 'campaign_managed_by') and campaign_request.campaign_managed_by is not None:
                setattr(existing_campaign, 'campaign_managed_by', campaign_request.campaign_managed_by)

            if hasattr(campaign_request, 'stage') and campaign_request.stage is not None:
                setattr(existing_campaign, 'stage', campaign_request.stage)

            if hasattr(campaign_request, 'type_of_content') and campaign_request.type_of_content is not None:
                setattr(existing_campaign, 'type_of_content', campaign_request.type_of_content)

            if hasattr(campaign_request, 'campaign_notes') and campaign_request.campaign_notes is not None:
                setattr(existing_campaign, 'campaign_notes', campaign_request.campaign_notes)

            if hasattr(campaign_request, 'rating') and campaign_request.rating is not None:
                setattr(existing_campaign, 'rating', campaign_request.rating)

            if hasattr(campaign_request, 'review') and campaign_request.review is not None:
                setattr(existing_campaign, 'review', campaign_request.review)

            if hasattr(campaign_request,
                       'influencer_finalization_date') and campaign_request.influencer_finalization_date is not None:
                setattr(existing_campaign, 'influencer_finalization_date',
                        campaign_request.influencer_finalization_date)

            if hasattr(campaign_request, 'content_shoot_date') and campaign_request.content_shoot_date is not None:
                setattr(existing_campaign, 'content_shoot_date', campaign_request.content_shoot_date)

            if hasattr(campaign_request, 'insta_post_link') and campaign_request.insta_post_link is not None:
                setattr(existing_campaign, 'insta_post_link', campaign_request.insta_post_link)

            if hasattr(campaign_request, 'yt_post_link') and campaign_request.yt_post_link is not None:
                setattr(existing_campaign, 'yt_post_link', campaign_request.yt_post_link)

            if hasattr(campaign_request, 'fb_post_link') and campaign_request.fb_post_link is not None:
                setattr(existing_campaign, 'fb_post_link', campaign_request.fb_post_link)

            if hasattr(campaign_request, 'content_post_date') and campaign_request.content_post_date is not None:
                setattr(existing_campaign, 'content_post_date', campaign_request.content_post_date)

            if hasattr(campaign_request,
                       'content_billing_amount') and campaign_request.content_billing_amount is not None:
                setattr(existing_campaign, 'content_billing_amount', campaign_request.content_billing_amount)

            if hasattr(campaign_request,
                       'content_billing_payment_at') and campaign_request.content_billing_payment_at is not None:
                setattr(existing_campaign, 'content_billing_payment_at', campaign_request.content_billing_payment_at)

            if hasattr(campaign_request,
                       'content_billing_payment_status') and campaign_request.content_billing_payment_status is not None:
                setattr(existing_campaign, 'content_billing_payment_status',
                        campaign_request.content_billing_payment_status)

            if hasattr(campaign_request, 'first_billing_date') and campaign_request.first_billing_date is not None:
                setattr(existing_campaign, 'first_billing_date', campaign_request.first_billing_date)

            if hasattr(campaign_request, 'first_billing_views') and campaign_request.first_billing_views is not None:
                setattr(existing_campaign, 'first_billing_views', campaign_request.first_billing_views)

            if hasattr(campaign_request, 'first_billing_likes') and campaign_request.first_billing_likes is not None:
                setattr(existing_campaign, 'first_billing_likes', campaign_request.first_billing_likes)

            if hasattr(campaign_request,
                       'first_billing_comments') and campaign_request.first_billing_comments is not None:
                setattr(existing_campaign, 'first_billing_comments', campaign_request.first_billing_comments)

            if hasattr(campaign_request, 'first_billing_shares') and campaign_request.first_billing_shares is not None:
                setattr(existing_campaign, 'first_billing_shares', campaign_request.first_billing_shares)

            if hasattr(campaign_request, 'first_billing_amount') and campaign_request.first_billing_amount is not None:
                setattr(existing_campaign, 'first_billing_amount', campaign_request.first_billing_amount)

            if hasattr(campaign_request,
                       'first_billing_payment_at') and campaign_request.first_billing_payment_at is not None:
                setattr(existing_campaign, 'first_billing_payment_at', campaign_request.first_billing_payment_at)

            if hasattr(campaign_request,
                       'first_billing_payment_status') and campaign_request.first_billing_payment_status is not None:
                setattr(existing_campaign, 'first_billing_payment_status',
                        campaign_request.first_billing_payment_status)

            if hasattr(campaign_request, 'second_billing_date') and campaign_request.second_billing_date is not None:
                setattr(existing_campaign, 'second_billing_date', campaign_request.second_billing_date)

            if hasattr(campaign_request, 'second_billing_views') and campaign_request.second_billing_views is not None:
                setattr(existing_campaign, 'second_billing_views', campaign_request.second_billing_views)

            if hasattr(campaign_request, 'second_billing_likes') and campaign_request.second_billing_likes is not None:
                setattr(existing_campaign, 'second_billing_likes', campaign_request.second_billing_likes)

            if hasattr(campaign_request,
                       'second_billing_comments') and campaign_request.second_billing_comments is not None:
                setattr(existing_campaign, 'second_billing_comments', campaign_request.second_billing_comments)

            if hasattr(campaign_request,
                       'second_billing_shares') and campaign_request.second_billing_shares is not None:
                setattr(existing_campaign, 'second_billing_shares', campaign_request.second_billing_shares)

            if hasattr(campaign_request,
                       'second_billing_amount') and campaign_request.second_billing_amount is not None:
                setattr(existing_campaign, 'second_billing_amount', campaign_request.second_billing_amount)

            if hasattr(campaign_request,
                       'second_billing_payment_at') and campaign_request.second_billing_payment_at is not None:
                setattr(existing_campaign, 'second_billing_payment_at', campaign_request.second_billing_payment_at)

            if hasattr(campaign_request,
                       'second_billing_payment_status') and campaign_request.second_billing_payment_status is not None:
                setattr(existing_campaign, 'second_billing_payment_status',
                        campaign_request.second_billing_payment_status)

            if hasattr(campaign_request, 'post_insights') and campaign_request.post_insights is not None:
                setattr(existing_campaign, 'post_insights', campaign_request.post_insights)

            if hasattr(campaign_request, 'pending_deliverables') and campaign_request.pending_deliverables is not None:
                setattr(existing_campaign, 'pending_deliverables', campaign_request.pending_deliverables)
            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(f"Unable to update campaign for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def update_campaign_to_influencer_finalization(self, campaign_id: int,
                                                   campaign_request: CampaignInfluencerFinalizedRequest) -> Optional[
        Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)
            setattr(existing_campaign, 'last_updated_by', campaign_request.campaign_managed_by)
            setattr(existing_campaign, 'campaign_managed_by', campaign_request.campaign_managed_by)
            setattr(existing_campaign, 'stage', CampaignStage.INFLUENCER_FINALIZED)
            setattr(existing_campaign, 'influencer_finalization_date', campaign_request.influencer_finalization_date)
            if hasattr(campaign_request, 'type_of_content') and campaign_request.type_of_content is not None:
                setattr(existing_campaign, 'type_of_content', campaign_request.type_of_content)

            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(
                f"Unable to update campaign to INFLUENCER_FINALIZED for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def update_campaign_to_shoot_completed(self, campaign_id: int, content_shoot_date: date) -> Optional[Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)
            setattr(existing_campaign, 'stage', CampaignStage.SHOOT_COMPLETED)
            setattr(existing_campaign, 'content_shoot_date', content_shoot_date)

            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(
                f"Unable to update campaign to SHOOT_COMPLETED for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def update_campaign_to_draft_approved(self, campaign_id: int, content_charge: int,
                                          draft_approved_date: date) -> Optional[Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)
            setattr(existing_campaign, 'content_draft_date', draft_approved_date)
            setattr(existing_campaign, 'content_billing_amount', content_charge)
            setattr(existing_campaign, 'stage', CampaignStage.DRAFT_APPROVED)
            setattr(existing_campaign, 'content_billing_payment_status', PaymentStatus.PENDING)

            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(
                f"Unable to update campaign to DRAFT_APPROVED for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def update_campaign_to_content_posted(self, campaign_id: int, campaign_request: CampaignContentPostRequest) -> \
            Optional[Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)
            setattr(existing_campaign, 'stage', CampaignStage.CONTENT_POSTED)
            setattr(existing_campaign, 'content_post_date', campaign_request.content_post_time)
            setattr(existing_campaign, 'content_billing_payment_status', campaign_request.payment_status)

            if hasattr(campaign_request, 'payment_time') and campaign_request.payment_time is not None:
                setattr(existing_campaign, 'content_billing_payment_at', campaign_request.payment_time)

            if hasattr(campaign_request, 'insta_post_link') and campaign_request.insta_post_link is not None:
                setattr(existing_campaign, 'insta_post_link', campaign_request.insta_post_link)

            if hasattr(campaign_request, 'yt_post_link') and campaign_request.yt_post_link is not None:
                setattr(existing_campaign, 'yt_post_link', campaign_request.yt_post_link)

            if hasattr(campaign_request, 'fb_post_link') and campaign_request.fb_post_link is not None:
                setattr(existing_campaign, 'fb_post_link', campaign_request.fb_post_link)

            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(
                f"Unable to update campaign to CONTENT_POSTED for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def update_campaign_to_day2_billing(self, campaign_id: int, reach_price: int,
                                        campaign_request: CampaignDay2BillingRequest) -> Optional[Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)
            setattr(existing_campaign, 'first_billing_date', campaign_request.day2_billing_date)
            setattr(existing_campaign, 'first_billing_amount', campaign_request.views * reach_price // 1000)
            setattr(existing_campaign, 'stage', CampaignStage.DAY2_BILLING)
            setattr(existing_campaign, 'first_billing_payment_status', PaymentStatus.PENDING)
            setattr(existing_campaign, 'first_billing_views', campaign_request.views)

            if hasattr(campaign_request, 'likes') and campaign_request.likes is not None:
                setattr(existing_campaign, 'first_billing_likes', campaign_request.likes)

            if hasattr(campaign_request, 'comments') and campaign_request.comments is not None:
                setattr(existing_campaign, 'first_billing_comments', campaign_request.comments)

            if hasattr(campaign_request, 'shares') and campaign_request.shares is not None:
                setattr(existing_campaign, 'first_billing_shares', campaign_request.shares)

            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(
                f"Unable to update campaign to DAY2_BILLING for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def update_campaign_to_day2_payment(self, campaign_id: int,
                                        campaign_request: CampaignDay2PaymentRequest) -> Optional[Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)
            setattr(existing_campaign, 'first_billing_payment_status', campaign_request.payment_status)

            if hasattr(campaign_request, 'payment_time') and campaign_request.payment_time is not None:
                setattr(existing_campaign, 'first_billing_payment_at', campaign_request.payment_time)

            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(
                f"Unable to update campaign to DAY2_PAYMENT for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def update_campaign_to_day8_billing(self, campaign_id: int, reach_price: int,
                                        campaign_request: CampaignDay8BillingRequest) -> Optional[Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)
            setattr(existing_campaign, 'second_billing_date', campaign_request.day8_billing_date)
            setattr(existing_campaign, 'second_billing_amount', campaign_request.views * reach_price // 1000)
            setattr(existing_campaign, 'stage', CampaignStage.DAY8_BILLING)
            setattr(existing_campaign, 'second_billing_payment_status', PaymentStatus.PENDING)
            setattr(existing_campaign, 'second_billing_views', campaign_request.views)

            if hasattr(campaign_request, 'likes') and campaign_request.likes is not None:
                setattr(existing_campaign, 'second_billing_likes', campaign_request.likes)

            if hasattr(campaign_request, 'comments') and campaign_request.comments is not None:
                setattr(existing_campaign, 'second_billing_comments', campaign_request.comments)

            if hasattr(campaign_request, 'shares') and campaign_request.shares is not None:
                setattr(existing_campaign, 'second_billing_shares', campaign_request.shares)

            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(
                f"Unable to update campaign to DAY8_BILLING for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def update_campaign_to_day8_payment(self, campaign_id: int,
                                        campaign_request: CampaignDay8PaymentRequest,
                                        post_insights: Optional[List[str]]) -> Optional[Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)
            setattr(existing_campaign, 'second_billing_payment_status', campaign_request.payment_status)
            setattr(existing_campaign, 'stage', CampaignStage.COMPLETED)

            if hasattr(campaign_request, 'payment_time') and campaign_request.payment_time is not None:
                setattr(existing_campaign, 'second_billing_payment_at', campaign_request.payment_time)

            if post_insights and len(post_insights) > 0:
                setattr(existing_campaign, 'post_insights', post_insights)

            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(
                f"Unable to update campaign to COMPLETED for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def update_campaign_to_cancelled(self, campaign_id: int) -> Optional[Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)
            setattr(existing_campaign, 'stage', CampaignStage.CANCELLED)

            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(
                f"Unable to update campaign to CANCELLED for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def update_campaign_pending_deliverables(self, campaign_id: int, pending_deliverables: List[str]) -> Optional[
        Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)
            if pending_deliverables and len(pending_deliverables) > 0:
                setattr(existing_campaign, 'pending_deliverables', pending_deliverables)

            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error(
                f"Unable to update pending deliverables for campaign_id {campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(campaign_id))

    def create_campaign_rating(self, rate_campaign: RateCampaign) -> Optional[Campaign]:

        existing_campaign = self.db.get(Campaign, rate_campaign.campaign_id)

        if not existing_campaign:
            return None

        setattr(existing_campaign, 'rating', rate_campaign.rating)
        setattr(existing_campaign, 'review', rate_campaign.comment)

        self.db.commit()
        self.db.refresh(existing_campaign)
        return existing_campaign

    def get_campaign_by_id(self, campaign_id: int) -> Campaign:
        return self.db.query(Campaign).filter(Campaign.id == campaign_id).first()

    def get_all_campaign_by_client(self, client_id: int) -> List[Campaign]:
        return self.db.query(Campaign).filter(Campaign.client_id == client_id).order_by(
            Campaign.last_updated_at.desc()).all()

    def get_all_running_campaign_with_an_influencer(self, client_id: int, influencer_id: int) -> List[Campaign]:
        return self.db.query(Campaign).filter(Campaign.client_id == client_id).filter(
            Campaign.influencer_id == influencer_id).all()

    def get_all_completed_campaign_for_an_influencer(self, influencer_id: int) -> List[Campaign]:
        return self.db.query(Campaign).filter(Campaign.influencer_id == influencer_id).filter(
            Campaign.stage == CampaignStage.COMPLETED).all()

    def get_all_active_campaigns(self) -> List[Campaign]:
        return self.db.query(Campaign).filter(Campaign.stage.in_(
            [CampaignStage.CREATED, CampaignStage.INFLUENCER_FINALIZED, CampaignStage.SHOOT_COMPLETED,
             CampaignStage.DRAFT_APPROVED,
             CampaignStage.CONTENT_POSTED, CampaignStage.DAY2_BILLING, CampaignStage.DAY8_BILLING])).all()
