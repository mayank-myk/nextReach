from typing import Optional

from pydantic import BaseModel


class InstagramDetail(BaseModel):
    username: str
    followers: Optional[str]
    city_1: Optional[int]
    city_pc_1: Optional[int]
    city_2: Optional[int]
    city_pc_2: Optional[int]
    city_3: Optional[int]
    city_pc_3: Optional[int]
    age_13_to_17: Optional[int]
    age_18_to_24: Optional[int]
    age_25_to_34: Optional[int]
    age_35_to_44: Optional[int]
    age_45_to_54: Optional[int]
    age_55: Optional[int]
    men_follower_pc: Optional[int]
    women_follower_pc: Optional[int]
    avg_views: Optional[str]
    max_views: Optional[str]
    min_views: Optional[str]
    consistency_score: Optional[int]
    avg_likes: Optional[str]
    avg_comments: Optional[str]
    avg_shares: Optional[str]
    engagement_rate: Optional[int]
