from typing import Optional

from pydantic import BaseModel, Field

from app.enums.city import City


class InfluencerMetricRequest(BaseModel):
    created_by: str = Field(..., min_length=3)
    influencer_id: int = Field(...)
    insta_followers: Optional[int] = Field(None, ge=0)
    insta_city_1: Optional[City] = None
    insta_city_pc_1: Optional[int] = Field(None, ge=0)
    insta_city_2: Optional[City] = None
    insta_city_pc_2: Optional[int] = Field(None, ge=0)
    insta_city_3: Optional[City] = None
    insta_city_pc_3: Optional[int] = Field(None, ge=0)
    insta_age_13_to_17: Optional[int] = Field(None, ge=0)
    insta_age_18_to_24: Optional[int] = Field(None, ge=0)
    insta_age_25_to_34: Optional[int] = Field(None, ge=0)
    insta_age_35_to_44: Optional[int] = Field(None, ge=0)
    insta_age_45_to_54: Optional[int] = Field(None, ge=0)
    insta_age_55: Optional[int] = Field(None, ge=0)
    insta_men_follower_pc: Optional[int] = Field(None, ge=0)
    insta_women_follower_pc: Optional[int] = Field(None, ge=0)
    insta_avg_views: Optional[int] = Field(None, ge=0)
    insta_max_views: Optional[int] = Field(None, ge=0)
    insta_min_views: Optional[int] = Field(None, ge=0)
    insta_consistency_score: Optional[int] = Field(None, ge=0)
    insta_avg_likes: Optional[int] = Field(None, ge=0)
    insta_avg_comments: Optional[int] = Field(None, ge=0)
    insta_avg_shares: Optional[int] = Field(None, ge=0)
    insta_engagement_rate: Optional[int] = Field(None, ge=0)
    yt_followers: Optional[int] = Field(None, ge=0)
    yt_city_1: Optional[City] = None
    yt_city_pc_1: Optional[int] = Field(None, ge=0)
    yt_city_2: Optional[City] = None
    yt_city_pc_2: Optional[int] = Field(None, ge=0)
    yt_city_3: Optional[City] = None
    yt_city_pc_3: Optional[int] = Field(None, ge=0)
    yt_avg_views: Optional[int] = Field(None, ge=0)
    yt_max_views: Optional[int] = Field(None, ge=0)
    yt_min_views: Optional[int] = Field(None, ge=0)
    yt_consistency_score: Optional[int] = Field(None, ge=0)
    yt_avg_likes: Optional[int] = Field(None, ge=0)
    yt_avg_comments: Optional[int] = Field(None, ge=0)
    yt_avg_shares: Optional[int] = Field(None, ge=0)
    yt_engagement_rate: Optional[int] = Field(None, ge=0)
    fb_followers: Optional[int] = Field(None, ge=0)
    fb_city_1: Optional[City] = None
    fb_city_pc_1: Optional[int] = Field(None, ge=0)
    fb_city_2: Optional[City] = None
    fb_city_pc_2: Optional[int] = Field(None, ge=0)
    fb_city_3: Optional[City] = None
    fb_city_pc_3: Optional[int] = Field(None, ge=0)
    fb_avg_views: Optional[int] = Field(None, ge=0)
    fb_max_views: Optional[int] = Field(None, ge=0)
    fb_min_views: Optional[int] = Field(None, ge=0)
    fb_consistency_score: Optional[int] = Field(None, ge=0)
    fb_avg_likes: Optional[int] = Field(None, ge=0)
    fb_avg_comments: Optional[int] = Field(None, ge=0)
    fb_avg_shares: Optional[int] = Field(None, ge=0)
    fb_engagement_rate: Optional[int] = Field(None, ge=0)
