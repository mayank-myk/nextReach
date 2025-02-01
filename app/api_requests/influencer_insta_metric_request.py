from typing import Optional

from pydantic import BaseModel, Field


class InfluencerInstaMetricRequest(BaseModel):
    created_by: str = Field(..., min_length=3)
    username: str = Field(..., max_length=255)
    profile_link: str = Field(..., max_length=255)
    followers: Optional[int] = Field(None, ge=0)
    city_1: Optional[str] = None
    city_pc_1: Optional[int] = Field(None, ge=0)
    city_2: Optional[str] = None
    city_pc_2: Optional[int] = Field(None, ge=0)
    city_3: Optional[str] = None
    city_pc_3: Optional[int] = Field(None, ge=0)
    age_13_to_17: Optional[int] = Field(None, ge=0)
    age_18_to_24: Optional[int] = Field(None, ge=0)
    age_25_to_34: Optional[int] = Field(None, ge=0)
    age_35_to_44: Optional[int] = Field(None, ge=0)
    age_45_to_54: Optional[int] = Field(None, ge=0)
    age_55: Optional[int] = Field(None, ge=0)
    men_follower_pc: Optional[int] = Field(None, ge=0)
    women_follower_pc: Optional[int] = Field(None, ge=0)
    avg_views: Optional[int] = Field(None, ge=0)
    max_views: Optional[int] = Field(None, ge=0)
    consistency_score: Optional[int] = Field(None, ge=0)
    avg_likes: Optional[int] = Field(None, ge=0)
    avg_comments: Optional[int] = Field(None, ge=0)
    avg_shares: Optional[int] = Field(None, ge=0)
    engagement_rate: Optional[float] = Field(None, ge=0)
