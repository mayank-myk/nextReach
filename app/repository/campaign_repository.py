from typing import List, Optional

from sqlalchemy.orm import Session

from app.database.campaign_table import Campaign
from app.enums.campaign_stage import CampaignStage
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.requests.campaign_request import CampaignRequest
from app.requests.rate_campaign import RateCampaign
from app.utils.logger import configure_logger

_log = configure_logger()


class CampaignRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_campaign(self, campaign_id: str, campaign_request: CampaignRequest) -> Campaign:
        new_campaign = Campaign(
            id=campaign_id,
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
            youtube_post_link=campaign_request.youtube_post_link,
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
            # third_billing_date=campaign_request.third_billing_date,
            # third_billing_views=campaign_request.third_billing_views,
            # third_billing_likes=campaign_request.third_billing_likes,
            # third_billing_comments=campaign_request.third_billing_comments,
            # third_billing_shares=campaign_request.third_billing_shares,
            # third_billing_amount=campaign_request.third_billing_amount,
            # third_billing_payment_at=campaign_request.third_billing_payment_at,
            # third_billing_payment_status=campaign_request.third_billing_payment_status,
            post_insights=campaign_request.post_insights,
            pending_deliverables=campaign_request.pending_deliverables
        )

        self.db.add(new_campaign)
        self.db.commit()
        self.db.refresh(new_campaign)
        return new_campaign

    def create_collab_campaign(self, campaign_id: str, client_id: str, influencer_id: str) -> Campaign:

        new_campaign = Campaign(
            id=campaign_id,
            created_by=client_id,
            campaign_managed_by='system',
            last_updated_by=client_id,
            influencer_id=influencer_id,
            client_id=client_id,
            stage=CampaignStage.CREATED
        )

        self.db.add(new_campaign)
        self.db.commit()
        self.db.refresh(new_campaign)
        return new_campaign

    def update_campaign(self, campaign_id: str, campaign_request: CampaignRequest) -> Optional[Campaign]:
        try:
            existing_campaign = self.db.get(Campaign, campaign_id)

            if not existing_campaign:
                return None

            if hasattr(CampaignRequest, 'created_by'):
                setattr(existing_campaign, 'last_updated_by', campaign_request.created_by)

            if hasattr(CampaignRequest, 'campaign_managed_by'):
                setattr(existing_campaign, 'campaign_managed_by', campaign_request.campaign_managed_by)

            if hasattr(CampaignRequest, 'stage'):
                setattr(existing_campaign, 'stage', campaign_request.stage)

            if hasattr(CampaignRequest, 'content_charge'):
                setattr(existing_campaign, 'content_charge', campaign_request.content_charge)

            if hasattr(CampaignRequest, 'views_charge'):
                setattr(existing_campaign, 'views_charge', campaign_request.views_charge)

            if hasattr(CampaignRequest, 'type_of_content'):
                setattr(existing_campaign, 'type_of_content', campaign_request.type_of_content)

            if hasattr(CampaignRequest, 'campaign_notes'):
                setattr(existing_campaign, 'campaign_notes', campaign_request.campaign_notes)

            if hasattr(CampaignRequest, 'rating'):
                setattr(existing_campaign, 'rating', campaign_request.rating)

            if hasattr(CampaignRequest, 'review'):
                setattr(existing_campaign, 'review', campaign_request.review)

            if hasattr(CampaignRequest, 'influencer_finalization_date'):
                setattr(existing_campaign, 'influencer_finalization_date',
                        campaign_request.influencer_finalization_date)

            if hasattr(CampaignRequest, 'content_shoot_date'):
                setattr(existing_campaign, 'content_shoot_date', campaign_request.content_shoot_date)

            if hasattr(CampaignRequest, 'insta_post_link'):
                setattr(existing_campaign, 'insta_post_link', campaign_request.insta_post_link)

            if hasattr(CampaignRequest, 'youtube_post_link'):
                setattr(existing_campaign, 'youtube_post_link', campaign_request.youtube_post_link)

            if hasattr(CampaignRequest, 'fb_post_link'):
                setattr(existing_campaign, 'fb_post_link', campaign_request.fb_post_link)

            if hasattr(CampaignRequest, 'content_post_date'):
                setattr(existing_campaign, 'content_post_date', campaign_request.content_post_date)

            if hasattr(CampaignRequest, 'content_billing_amount'):
                setattr(existing_campaign, 'content_billing_amount', campaign_request.content_billing_amount)

            if hasattr(CampaignRequest, 'content_billing_payment_at'):
                setattr(existing_campaign, 'content_billing_payment_at', campaign_request.content_billing_payment_at)

            if hasattr(CampaignRequest, 'content_billing_payment_status'):
                setattr(existing_campaign, 'content_billing_payment_status',
                        campaign_request.content_billing_payment_status)

            if hasattr(CampaignRequest, 'first_billing_date'):
                setattr(existing_campaign, 'first_billing_date', campaign_request.first_billing_date)

            if hasattr(CampaignRequest, 'first_billing_views'):
                setattr(existing_campaign, 'first_billing_views', campaign_request.first_billing_views)

            if hasattr(CampaignRequest, 'first_billing_likes'):
                setattr(existing_campaign, 'first_billing_likes', campaign_request.first_billing_likes)

            if hasattr(CampaignRequest, 'first_billing_comments'):
                setattr(existing_campaign, 'first_billing_comments', campaign_request.first_billing_comments)

            if hasattr(CampaignRequest, 'first_billing_shares'):
                setattr(existing_campaign, 'first_billing_shares', campaign_request.first_billing_shares)

            if hasattr(CampaignRequest, 'first_billing_amount'):
                setattr(existing_campaign, 'first_billing_amount', campaign_request.first_billing_amount)

            if hasattr(CampaignRequest, 'first_billing_payment_at'):
                setattr(existing_campaign, 'first_billing_payment_at', campaign_request.first_billing_payment_at)

            if hasattr(CampaignRequest, 'first_billing_payment_status'):
                setattr(existing_campaign, 'first_billing_payment_status',
                        campaign_request.first_billing_payment_status)

            if hasattr(CampaignRequest, 'second_billing_date'):
                setattr(existing_campaign, 'second_billing_date', campaign_request.second_billing_date)

            if hasattr(CampaignRequest, 'second_billing_views'):
                setattr(existing_campaign, 'second_billing_views', campaign_request.second_billing_views)

            if hasattr(CampaignRequest, 'second_billing_likes'):
                setattr(existing_campaign, 'second_billing_likes', campaign_request.second_billing_likes)

            if hasattr(CampaignRequest, 'second_billing_comments'):
                setattr(existing_campaign, 'second_billing_comments', campaign_request.second_billing_comments)

            if hasattr(CampaignRequest, 'second_billing_shares'):
                setattr(existing_campaign, 'second_billing_shares', campaign_request.second_billing_shares)

            if hasattr(CampaignRequest, 'second_billing_amount'):
                setattr(existing_campaign, 'second_billing_amount', campaign_request.second_billing_amount)

            if hasattr(CampaignRequest, 'second_billing_payment_at'):
                setattr(existing_campaign, 'second_billing_payment_at', campaign_request.second_billing_payment_at)

            if hasattr(CampaignRequest, 'second_billing_payment_status'):
                setattr(existing_campaign, 'second_billing_payment_status',
                        campaign_request.second_billing_payment_status)

            if hasattr(CampaignRequest, 'post_insights'):
                setattr(existing_campaign, 'post_insights', campaign_request.post_insights)

            if hasattr(CampaignRequest, 'pending_deliverables'):
                setattr(existing_campaign, 'pending_deliverables', campaign_request.pending_deliverables)
            self.db.commit()
            self.db.refresh(existing_campaign)
            return existing_campaign

        except Exception as ex:
            _log.error("Unable to update campaign for campaign_id {}".format(campaign_id))
            raise FetchOneUserMetadataException(ex, campaign_id)

    def create_campaign_rating(self, rate_campaign: RateCampaign) -> Optional[Campaign]:

        existing_campaign = self.db.get(Campaign, rate_campaign.campaign_id)

        if not existing_campaign:
            return None

        setattr(existing_campaign, 'rating', rate_campaign.rating)
        setattr(existing_campaign, 'review', rate_campaign.comment)

        self.db.commit()
        self.db.refresh(existing_campaign)
        return existing_campaign

    def get_campaign_by_id(self, campaign_id: str) -> Campaign:
        return self.db.query(Campaign).filter(Campaign.id == campaign_id).first()

    def get_all_campaign_for_a_user(self, client_id: str) -> List[Campaign]:
        return self.db.query(Campaign).filter(Campaign.client_id == client_id).all()
