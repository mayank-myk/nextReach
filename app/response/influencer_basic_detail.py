from typing import Optional, List

from pydantic import BaseModel

from app.enums.city import City
from app.enums.niche import Niche


class InfluencerBasicDetail(BaseModel):
    id: int
    name: str
    profile_picture: str
    niche: List[Niche]
    city: City
    profile_visited: bool
    views_charge: Optional[int] = None
    content_charge: Optional[int] = None
    insta_followers: Optional[str] = None
    yt_followers: Optional[str] = None
