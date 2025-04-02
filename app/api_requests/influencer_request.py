from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.gender import Gender
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform


class InfluencerRequest(BaseModel):
    created_by: str = Field(..., min_length=3)
    primary_platform: Platform
    name: str = Field(..., min_length=3)
    gender: Gender
    phone_number: str = Field(..., min_length=10, max_length=10)
    email: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=255)
    upi_id: Optional[str] = Field(None, max_length=255)
    languages: List[Language]
    next_reach_score: int = Field(..., ge=0)
    dob: Optional[date] = None
    niche: List[Niche]
    city: City
    collab_type: CollabType
    deliverables: Optional[List[str]] = None
    # content_charge: int = Field(..., ge=0)
    # views_charge: int = Field(..., ge=0)
    fixed_charge: int = Field(..., ge=0)
