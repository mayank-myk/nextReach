from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.enums.payment_status import PaymentStatus


class CampaignContentPostRequest(BaseModel):
    content_post_time: datetime
    insta_post_link: Optional[str] = Field(None, max_length=255)
    yt_post_link: Optional[str] = Field(None, max_length=255)
    fb_post_link: Optional[str] = Field(None, max_length=255)
    payment_time: Optional[datetime] = None
    payment_status: PaymentStatus

