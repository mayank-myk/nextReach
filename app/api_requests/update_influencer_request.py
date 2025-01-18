from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.gender import Gender
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform


class UpdateInfluencerRequest(BaseModel):
    updated_by: str = Field(..., min_length=3)
    primary_platform: Optional[Platform] = None
    name: Optional[str] = Field(None, max_length=255)
    gender: Optional[Gender] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=10)
    email: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=255)
    profile_picture: Optional[str] = Field(None, min_length=5)
    languages: Optional[List[Language]] = None
    next_reach_score: Optional[int] = Field(None, ge=0)
    dob: Optional[date] = None
    niche: Optional[List[Niche]] = None
    city: Optional[City] = None
    collab_type: Optional[CollabType] = None
    deliverables: Optional[List[str]] = None
    content_charge: Optional[int] = Field(None, ge=0)
    views_charge: Optional[int] = Field(None, ge=0)
