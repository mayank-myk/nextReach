from typing import Optional

from pydantic import BaseModel

from app.response.facebook_detail import FacebookDetail
from app.response.instagram_detail import InstagramDetail
from app.response.youtube_detail import YouTubeDetail


class InfluencerMetricDetail(BaseModel):
    insta_detail: Optional[InstagramDetail]
    yt_detail: Optional[YouTubeDetail]
    fb_detail: Optional[FacebookDetail]
