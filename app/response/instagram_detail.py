from typing import Optional

from pydantic import BaseModel


class InstagramDetail(BaseModel):
    username: str
    followers: Optional[int]
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
    avg_views: Optional[int]
    max_views: Optional[int]
    min_views: Optional[int]
    spread: Optional[int]
    avg_likes: Optional[int]
    avg_comments: Optional[int]
    avg_shares: Optional[int]
    engagement_rate: Optional[int]
