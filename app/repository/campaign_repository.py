from typing import List
from sqlalchemy.orm import Session
from app.database.campaign_table import Campaign
from app.models.campaign_stage import CampaignStage
from app.models.status import Status
from app.requests.campaign_request import CampaignRequest
from app.requests.rate_campaign import RateCampaign


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
            status=Status.PROCESSING,
            stage=CampaignStage.INFLUENCER_FINALIZATION,
            content_charge=campaign_request.content_charge,
            views_charge=campaign_request.views_charge,
            influencer_avg_views=campaign_request.influencer_avg_views,
            influencer_followers=campaign_request.influencer_followers,
            type_of_content=campaign_request.type_of_content,
            campaign_notes=campaign_request.campaign_notes,
            insta_post_link=campaign_request.insta_post_link,
            youtube_post_link=campaign_request.youtube_post_link,
            fb_post_link=campaign_request.fb_post_link,
            rating=campaign_request.rating,
            review=campaign_request.review,
            content_shoot_date=campaign_request.content_shoot_date,
            content_billing_amount=campaign_request.content_billing_amount,
            content_billing_payment_at=campaign_request.content_billing_payment_at,
            content_billing_payment_status=campaign_request.content_billing_payment_status,
            first_billing_views=campaign_request.first_billing_views,
            first_billing_likes=campaign_request.first_billing_likes,
            first_billing_comments=campaign_request.first_billing_comments,
            first_billing_shares=campaign_request.first_billing_shares,
            first_billing_amount=campaign_request.first_billing_amount,
            first_billing_payment_at=campaign_request.first_billing_payment_at,
            first_billing_payment_status=campaign_request.first_billing_payment_status,
            second_billing_views=campaign_request.second_billing_views,
            second_billing_likes=campaign_request.second_billing_likes,
            second_billing_comments=campaign_request.second_billing_comments,
            second_billing_shares=campaign_request.second_billing_shares,
            second_billing_amount=campaign_request.second_billing_amount,
            second_billing_payment_at=campaign_request.second_billing_payment_at,
            second_billing_payment_status=campaign_request.second_billing_payment_status,
            third_billing_views=campaign_request.third_billing_views,
            third_billing_likes=campaign_request.third_billing_likes,
            third_billing_comments=campaign_request.third_billing_comments,
            third_billing_shares=campaign_request.third_billing_shares,
            third_billing_amount=campaign_request.third_billing_amount,
            third_billing_payment_at=campaign_request.third_billing_payment_at,
            third_billing_payment_status=campaign_request.third_billing_payment_status,
        )

        self.db.add(new_campaign)
        self.db.commit()
        self.db.refresh(new_campaign)
        return new_campaign

    def create_collab_campaign(self, campaign_id: str, client_id: str, influencer_id: str) -> Campaign:

        new_campaign = Campaign(
            id=campaign_id,
            created_by=client_id,
            last_updated_by=client_id,
            influencer_id=influencer_id,
            client_id=client_id,
            status=Status.PROCESSING
        )

        self.db.add(new_campaign)
        self.db.commit()
        self.db.refresh(new_campaign)
        return new_campaign

    def update_campaign(self, campaign_id: str, campaign_request: CampaignRequest) -> Campaign:
        existing_campaign = await self.db.get(Campaign, campaign_id)

        if not existing_campaign:
            raise ValueError(f"Campaign with id {campaign_id} not found")

        db_campaign = Campaign(
            id=existing_campaign.id,
            created_by=existing_campaign.created_by,
            last_updated_by=campaign_request.created_by,
            campaign_managed_by=existing_campaign.campaign_managed_by,
            influencer_id=existing_campaign.influencer_id,
            client_id=existing_campaign.client_id,
            stage=campaign_request.stage,
            content_charge=campaign_request.content_charge,
            views_charge=campaign_request.views_charge,
            influencer_avg_views=campaign_request.influencer_avg_views,
            influencer_followers=campaign_request.influencer_followers,
            type_of_content=campaign_request.type_of_content,
            campaign_notes=campaign_request.campaign_notes,
            insta_post_link=campaign_request.insta_post_link,
            youtube_post_link=campaign_request.youtube_post_link,
            fb_post_link=campaign_request.fb_post_link,
            rating=campaign_request.rating,
            review=campaign_request.review,
            content_shoot_date=campaign_request.content_shoot_date,
            content_billing_amount=campaign_request.content_billing_amount,
            content_billing_payment_at=campaign_request.content_billing_payment_at,
            content_billing_payment_status=campaign_request.content_billing_payment_status,
            first_billing_views=campaign_request.first_billing_views,
            first_billing_likes=campaign_request.first_billing_likes,
            first_billing_comments=campaign_request.first_billing_comments,
            first_billing_shares=campaign_request.first_billing_shares,
            first_billing_amount=campaign_request.first_billing_amount,
            first_billing_payment_at=campaign_request.first_billing_payment_at,
            first_billing_payment_status=campaign_request.first_billing_payment_status,
            second_billing_views=campaign_request.second_billing_views,
            second_billing_likes=campaign_request.second_billing_likes,
            second_billing_comments=campaign_request.second_billing_comments,
            second_billing_shares=campaign_request.second_billing_shares,
            second_billing_amount=campaign_request.second_billing_amount,
            second_billing_payment_at=campaign_request.second_billing_payment_at,
            second_billing_payment_status=campaign_request.second_billing_payment_status,
            third_billing_views=campaign_request.third_billing_views,
            third_billing_likes=campaign_request.third_billing_likes,
            third_billing_comments=campaign_request.third_billing_comments,
            third_billing_shares=campaign_request.third_billing_shares,
            third_billing_amount=campaign_request.third_billing_amount,
            third_billing_payment_at=campaign_request.third_billing_payment_at,
            third_billing_payment_status=campaign_request.third_billing_payment_status,
        )

        self.db.commit()
        self.db.refresh(db_campaign)
        return db_campaign

    def create_campaign_rating(self, rate_campaign: RateCampaign) -> Campaign:

        existing_campaign = await self.db.get(Campaign, rate_campaign.campaign_id)

        if not existing_campaign:
            raise ValueError(f"Campaign with id {rate_campaign.campaign_id} not found")

        if existing_campaign.client.id != rate_campaign.user_id:
            raise ValueError(f"Client Id not matching")

        setattr(existing_campaign, 'rating', rate_campaign.rating)
        setattr(existing_campaign, 'review', rate_campaign.comment)

        self.db.commit()
        self.db.refresh(existing_campaign)
        return existing_campaign

    def get_campaign_by_id(self, campaign_id: str) -> Campaign:
        """Get influencer by ID."""
        return self.db.query(Campaign).filter(Campaign.id == campaign_id).first()

    def get_all_campaign_for_a_user(self, client_id: str) -> List[Campaign]:
        """Get influencer by ID."""
        return self.db.query(Campaign).filter(Campaign.client_id == client_id).all()
