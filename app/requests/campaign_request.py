import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.campaign_stage import CampaignStage
from app.models.content_type import ContentType
from app.models.status import Status


class CampaignRequest(BaseModel):
    created_by: str = Field(min_length=5, max_length=255)
    campaign_managed_by: Optional[Field(max_length=255)]
    influencer_id: str = Field(min_length=13, max_length=13)
    client_id: str = Field(min_length=13, max_length=13)
    stage: CampaignStage
    content_charge: Optional[Field(ge=0)]
    views_charge: Optional[Field(ge=0)]
    type_of_content: Optional[ContentType]
    campaign_notes: Optional[str]
    rating: Optional[Field(ge=0, le=5)]
    review: Optional[Field(max_length=255)]
    influencer_finalization_date: Optional[datetime]
    content_shoot_date: Optional[datetime]
    insta_post_link: Optional[Field(max_length=255)]
    youtube_post_link: Optional[Field(max_length=255)]
    fb_post_link: Optional[Field(max_length=255)]
    content_post_date: Optional[datetime]
    content_billing_amount: Optional[Field(ge=0)]
    content_billing_payment_at: Optional[datetime]
    content_billing_payment_status: Optional[Status]
    first_billing_date: Optional[datetime]
    first_billing_views: Optional[Field(ge=0)]
    first_billing_likes: Optional[Field(ge=0)]
    first_billing_comments: Optional[Field(ge=0)]
    first_billing_shares: Optional[Field(ge=0)]
    first_billing_amount: Optional[Field(ge=0)]
    first_billing_payment_at: Optional[datetime]
    first_billing_payment_status: Optional[Status]
    second_billing_date: Optional[datetime]
    second_billing_views: Optional[Field(ge=0)]
    second_billing_likes: Optional[Field(ge=0)]
    second_billing_comments: Optional[Field(ge=0)]
    second_billing_shares: Optional[Field(ge=0)]
    second_billing_amount: Optional[Field(ge=0)]
    second_billing_payment_at: Optional[datetime]
    second_billing_payment_status: Optional[Status]
    # third_billing_date: Optional[datetime]
    # third_billing_views: Optional[Field(ge=0)]
    # third_billing_likes: Optional[Field(ge=0)]
    # third_billing_comments: Optional[Field(ge=0)]
    # third_billing_shares: Optional[Field(ge=0)]
    # third_billing_amount: Optional[Field(ge=0)]
    # third_billing_payment_at: Optional[datetime]
    # third_billing_payment_status: Optional[Status]
    post_insights: Optional[List[str]]
    pending_deliverables: Optional[List[str]]
