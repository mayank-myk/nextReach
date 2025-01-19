from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CampaignContentPostRequest(BaseModel):
    content_post_date: datetime
    insta_post_link: Optional[str] = Field(None, max_length=255)
    yt_post_link: Optional[str] = Field(None, max_length=255)
    fb_post_link: Optional[str] = Field(None, max_length=255)
