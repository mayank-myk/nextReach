from typing import List, Optional

from pydantic import BaseModel


class CampaignDetailDump(BaseModel):
    campaign_id: int
    last_updated_at: Optional[str] = None
    stage: str
    ageing_day: Optional[int]

    client_id: int
    client_phone_number: str

    influencer_id: int
    influencer_name: Optional[str] = None
    insta_username: Optional[str] = None
    content_charge: int
    views_charge: int
    fixed_charge: int

    influencer_finalization_date: Optional[str] = None
    content_shoot_date: Optional[str] = None
    content_draft_date: Optional[str] = None
    content_billing_amount: Optional[int] = None
    content_billing_payment_at: Optional[str] = None
    content_billing_payment_status: Optional[str] = None

    content_post_date: Optional[str] = None
    insta_post_link: Optional[str] = None
    yt_post_link: Optional[str] = None
    fb_post_link: Optional[str] = None

    first_billing_date: Optional[str] = None
    first_billing_views: Optional[int] = None
    first_billing_likes: Optional[int] = None
    first_billing_comments: Optional[int] = None
    first_billing_shares: Optional[int] = None
    first_billing_amount: Optional[int] = None
    first_billing_payment_at: Optional[str] = None
    first_billing_payment_status: Optional[str] = None

    second_billing_date: Optional[str] = None
    second_billing_views: Optional[int] = None
    second_billing_likes: Optional[int] = None
    second_billing_comments: Optional[int] = None
    second_billing_shares: Optional[int] = None
    second_billing_amount: Optional[int] = None
    second_billing_payment_at: Optional[str] = None
    second_billing_payment_status: Optional[str] = None

    campaign_notes: Optional[str] = None
    post_insights: Optional[List[str]] = None
    pending_deliverables: Optional[List[str]] = None
