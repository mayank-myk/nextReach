from typing import Optional

from pydantic import BaseModel, Field

from app.enums.business_category import BusinessCategory
from app.enums.city import City
from app.enums.niche import Niche


class UpdateClientRequest(BaseModel):
    updated_by: str = Field(..., min_length=1)  # Enforcing str type with a length constraint
    name: Optional[str] = Field(None, max_length=255)  # Optional, but must be str if provided
    business_name: Optional[str] = Field(None, max_length=255)  # Optional, but must be str if provided
    email: Optional[str] = Field(None, max_length=255)  # Optional, but must be str if provided
    city: Optional[City] = None  # Optional, must be of type City if provided
    niche: Optional[Niche] = None  # Optional, must be of type Niche if provided
    category: Optional[BusinessCategory] = None  # Optional, must be of type BusinessCategory if provided
    insta_username: Optional[str] = Field(None, max_length=255)  # Optional, must be str if provided
    insta_profile_link: Optional[str] = Field(None, max_length=255)  # Optional, must be str if provided
    insta_followers: Optional[int] = Field(None, ge=0)  # Optional, but must be int >= 0 if provided
    yt_username: Optional[str] = Field(None, max_length=255)  # Optional, must be str if provided
    yt_profile_link: Optional[str] = Field(None, max_length=255)  # Optional, must be str if provided
    yt_followers: Optional[int] = Field(None, ge=0)  # Optional, but must be int >= 0 if provided
    fb_username: Optional[str] = Field(None, max_length=255)  # Optional, must be str if provided
    fb_profile_link: Optional[str] = Field(None, max_length=255)  # Optional, must be str if provided
    fb_followers: Optional[int] = Field(None, ge=0)  # Optional, but must be int >= 0 if provided
