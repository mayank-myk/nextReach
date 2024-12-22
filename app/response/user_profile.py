from pydantic import BaseModel, Field

from app.models.business_category import BusinessCategory
from app.models.city import City
from app.models.niche import Niche


class UserProfile(BaseModel):
    id: str
    name: str
    profile_picture: str
    business_name: str
    email: str
    city: City
    niche: Niche
    category: BusinessCategory
    total_profile_visited: int
    balance_profile_visits: int
    insta_username: str
    yt_username: str
    fb_username: str
