from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.enums.campaign_stage import CampaignStage
from app.enums.content_type import ContentType
from app.enums.payment_status import PaymentStatus


class CampaignRequest(BaseModel):
    created_by: str = Field(..., min_length=3, max_length=255)  # Required field
    campaign_managed_by: str = Field(..., max_length=255)  # Required field
    influencer_id: int = Field(...)  # Required field
    user_id: int = Field(...)  # Required field
    stage: CampaignStage  # Required field (assuming it's an enum)
    content_charge: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    views_charge: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    type_of_content: Optional[ContentType] = None  # Optional enum
    campaign_notes: Optional[str] = None  # Optional string
    rating: Optional[int] = Field(None, ge=0, le=5)  # Optional, but must be int between 0 and 5
    review: Optional[str] = Field(None, max_length=255)  # Optional string
    influencer_finalization_date: Optional[datetime] = None  # Optional datetime
    content_shoot_date: Optional[datetime] = None  # Optional datetime
    insta_post_link: Optional[str] = Field(None, max_length=255)  # Optional string
    yt_post_link: Optional[str] = Field(None, max_length=255)  # Optional string
    fb_post_link: Optional[str] = Field(None, max_length=255)  # Optional string
    content_post_date: Optional[datetime] = None  # Optional datetime
    content_billing_amount: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    content_billing_payment_at: Optional[datetime] = None  # Optional datetime
    content_billing_payment_status: Optional[PaymentStatus] = None  # Optional enum
    first_billing_date: Optional[datetime] = None  # Optional datetime
    first_billing_views: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    first_billing_likes: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    first_billing_comments: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    first_billing_shares: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    first_billing_amount: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    first_billing_payment_at: Optional[datetime] = None  # Optional datetime
    first_billing_payment_status: Optional[PaymentStatus] = None  # Optional enum
    second_billing_date: Optional[datetime] = None  # Optional datetime
    second_billing_views: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    second_billing_likes: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    second_billing_comments: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    second_billing_shares: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    second_billing_amount: Optional[int] = Field(None, ge=0)  # Optional, but must be int if provided
    second_billing_payment_at: Optional[datetime] = None  # Optional datetime
    second_billing_payment_status: Optional[PaymentStatus] = None  # Optional enum
    post_insights: Optional[List[str]] = None  # Optional list of strings
    pending_deliverables: Optional[List[str]] = None  # Optional list of strings
