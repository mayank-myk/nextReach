from typing import List, Optional

from pydantic import BaseModel, Field

from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.gender import Gender
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform


class InfluencerRequest(BaseModel):
    created_by: str = Field(..., min_length=5)
    primary_platform: Platform
    name: str = Field(..., min_length=5)
    gender: Gender
    phone_number: str = Field(..., min_length=10, max_length=10)
    email: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=255)
    profile_picture: str = Field(..., min_length=5)
    languages: List[Language]
    next_reach_score: int = Field(..., ge=0)
    age: int = Field(None, ge=0)
    insta_username: Optional[str] = Field(None, max_length=255)
    insta_profile_link: Optional[str] = Field(None, max_length=255)
    youtube_username: Optional[str] = Field(None, max_length=255)
    youtube_profile_link: Optional[str] = Field(None, max_length=255)
    fb_username: Optional[str] = Field(None, max_length=255)
    fb_profile_link: Optional[str] = Field(None, max_length=255)
    niche: Niche
    city: City
    collab_type: CollabType
    deliverables: Optional[List[str]] = None
    content_charge: int = Field(..., ge=0)
    views_charge: int = Field(..., ge=0)
