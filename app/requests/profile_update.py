from typing import Optional

from pydantic import BaseModel, Field

from app.enums.business_category import BusinessCategory
from app.enums.city import City
from app.enums.niche import Niche


class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    business_name: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    city: Optional[City] = None
    niche: Optional[Niche] = None
    category: Optional[BusinessCategory] = None
    insta_username: Optional[str] = Field(None, max_length=255)
    yt_username: Optional[str] = Field(None, max_length=255)
    fb_username: Optional[str] = Field(None, max_length=255)
