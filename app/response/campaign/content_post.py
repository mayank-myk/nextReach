import datetime
from typing import Optional

from pydantic import BaseModel

from app.response.campaign.billing_info import BillingInfo


class ContentPost(BaseModel):
    date: Optional[datetime.datetime] = None
    insta_post_link:  Optional[int] = None
    youtube_post_link:  Optional[int] = None
    fb_post_link:  Optional[int] = None
    billing_info: BillingInfo
