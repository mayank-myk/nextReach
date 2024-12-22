import datetime

from pydantic import BaseModel

from app.response.campaign.billing_info import BillingInfo


class ContentPost(BaseModel):
    date: datetime.datetime
    insta_post_link: str
    youtube_post_link: str
    fb_post_link: str
    billing_info: BillingInfo
