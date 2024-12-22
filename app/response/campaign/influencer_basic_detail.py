from pydantic import BaseModel

from app.enums.city import City
from app.enums.niche import Niche


class InfluencerBasicDetail(BaseModel):
    id: str
    name: str
    profile_picture: str
    niche: Niche
    city: City
    views_charge: int
    content_charge: int
