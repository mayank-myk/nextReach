from pydantic import BaseModel, Field

from app.models.city import City
from app.models.niche import Niche


class InfluencerBasicDetail(BaseModel):
    id: str
    name: str
    profile_picture: str
    niche: Niche
    city: City
    views_charge: int
    content_charge: int
