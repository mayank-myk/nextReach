from typing import Optional

from pydantic import BaseModel

from app.response.influencer.facebook_detail import FacebookDetail
from app.response.influencer.instagram_detail import InstagramDetail
from app.response.influencer.youtube_detail import YouTubeDetail


class InfluencerMetricDetail(BaseModel):
    insta_detail: Optional[InstagramDetail]
    yt_detail: Optional[YouTubeDetail]
    fb_detail: Optional[FacebookDetail]
