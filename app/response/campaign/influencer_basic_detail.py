from pydantic import BaseModel, Field

from app.models.city import City
from app.models.niche import Niche


class InfluencerBasicDetail(BaseModel):
    id: str = Field(min_length=13, max_length=13)
    name: str = Field(min_length=5)
    profile_picture: str
    niche: Niche
    city: City
    views_charge: int
    content_charge: int
