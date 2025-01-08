from typing import Optional

from pydantic import BaseModel

from app.response.campaign.billing_info import BillingInfo


class ContentPost(BaseModel):
    date: Optional[str] = None
    insta_post_link: Optional[str] = None
    yt_post_link: Optional[str] = None
    fb_post_link: Optional[str] = None
    billing_info: BillingInfo
