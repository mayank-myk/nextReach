from typing import Optional

from pydantic import BaseModel

from app.enums.business_category import BusinessCategory
from app.enums.city import City
from app.enums.niche import Niche


class ClientProfile(BaseModel):
    id: int
    name: Optional[str] = None
    phone_number: str
    profile_picture: Optional[str] = None
    business_name: Optional[str] = None
    email: Optional[str] = None
    city: Optional[City]
    niche: Optional[Niche]
    category: Optional[BusinessCategory]
    total_profile_visited: int
    balance_profile_visits: int
    insta_username: Optional[str] = None
    yt_username: Optional[str] = None
    fb_username: Optional[str] = None
