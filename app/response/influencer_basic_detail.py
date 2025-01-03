from typing import Optional

from pydantic import BaseModel

from app.enums.city import City
from app.enums.niche import Niche


class InfluencerBasicDetail(BaseModel):
    id: int
    name: str
    profile_picture: str
    niche: Niche
    city: City
    profile_visited: bool
    views_charge: Optional[int] = None
    content_charge: Optional[int] = None
    instagram_followers: Optional[str] = None
    youtube_followers: Optional[str] = None
