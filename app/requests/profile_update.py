from pydantic import BaseModel, Field

from app.models.business_category import BusinessCategory
from app.models.city import City
from app.models.niche import Niche


class ProfileUpdate(BaseModel):
    name: str
    business_name: str
    email: str
    city: City
    niche: Niche
    category: BusinessCategory
    insta_username: str
    yt_username: str
    fb_username: str
