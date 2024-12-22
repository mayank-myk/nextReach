import datetime
from typing import List

from pydantic import BaseModel, Field

from app.models.city import City
from app.models.collab_type import CollabType
from app.models.gender import Gender
from app.models.language import Language
from app.models.niche import Niche
from app.models.platform import Platform
from app.response.facebook_detail import FacebookDetail
from app.response.instagram_detail import InstagramDetail
from app.response.youtube_detail import YouTubeDetail


class InfluencerDetail(BaseModel):
    id: str = Field(min_length=13, max_length=13)
    last_updated_at: datetime.datetime
    profile_visited: bool
    primary_platform: Platform
    name: str = Field(min_length=5)
    gender: Gender
    profile_picture: str
    languages: List[Language]
    next_reach_score: int = Field(ge=0)
    niche: Niche
    city: City
    collab_type: CollabType
    deliverables: List[str]
    content_charge: int = Field(ge=0)
    views_charge: int = Field(ge=0)
    instagram_detail: InstagramDetail
    youtube_detail: YouTubeDetail
    facebook_detail: FacebookDetail
