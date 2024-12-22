import datetime
from typing import List

from pydantic import BaseModel, Field

from app.models.campaign_stage import CampaignStage
from app.models.content_type import ContentType
from app.models.status import Status


class CampaignDetail(BaseModel):
    id: str = Field(min_length=13, max_length=13)
    created_at: datetime.datetime
    last_updated_at: datetime.datetime
    created_by: str = Field(min_length=5, frozen=True)
    last_updated_by: str = Field(min_length=5, frozen=True)
    campaign_managed_by: str = Field(min_length=5, frozen=True)
    influencer_id: str = Field(min_length=13, max_length=13)
    client_id: str = Field(min_length=13, max_length=13)
    stage: CampaignStage
    content_charge: int = Field(ge=0, frozen=True)
    views_charge: int = Field(ge=0, frozen=True)
    influencer_avg_views: int = Field(ge=0, frozen=True)
    influencer_followers: int = Field(ge=0, frozen=True)
    collab: bool
    type_of_content: ContentType
    length_of_content: int = Field(ge=0)
    campaign_notes: str = Field(min_length=5)
    insta_post_link: str = Field(min_length=5)
    youtube_post_link: str = Field(min_length=5)
    fb_post_link: str = Field(min_length=5)
    rating: int
    review: str
    content_shoot_date: datetime.datetime
    content_billing_amount: int
    content_billing_payment_at: datetime.datetime
    content_billing_payment_status: Status
    first_billing_views: int
    first_billing_likes: int
    first_billing_comments: int
    first_billing_shares: int
    first_billing_amount: int
    first_billing_payment_at: datetime.datetime
    first_billing_payment_status: Status
    second_billing_views: int
    second_billing_likes: int
    second_billing_comments: int
    second_billing_shares: int
    second_billing_amount: int
    second_billing_payment_at: datetime.datetime
    second_billing_payment_status: Status
    third_billing_views: int
    third_billing_likes: int
    third_billing_comments: int
    third_billing_shares: int
    third_billing_amount: int
    third_billing_payment_at: datetime.datetime
    third_billing_payment_status: Status
    post_insights: List[str]
    pending_deliverables: List[str]
