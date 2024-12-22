from typing import Optional
from pydantic import BaseModel, Field
from app.models.business_category import BusinessCategory
from app.models.city import City
from app.models.niche import Niche


class ClientRequest(BaseModel):
    created_by: str = Field(min_length=5)
    name: str = Field(min_length=3, max_length=255)
    phone_number: str = Field(min_length=10, max_length=10)
    business_name: Optional[Field(max_length=255)]
    email: Optional[Field(max_length=255)]
    city: Optional[City]
    niche: Optional[Niche]
    category: Optional[BusinessCategory]
    balance_profile_visits: Optional[Field(ge=0)]
    insta_username: Optional[Field(max_length=255)]
    insta_profile_link: Optional[Field(max_length=255)]
    insta_followers: Optional[Field(ge=0)]
    yt_username: Optional[Field(max_length=255)]
    yt_profile_link: Optional[Field(max_length=255)]
    yt_followers: Optional[Field(ge=0)]
    fb_username: Optional[Field(max_length=255)]
    fb_profile_link: Optional[Field(max_length=255)]
    fb_followers: Optional[Field(ge=0)]
