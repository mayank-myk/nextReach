from typing import Optional

from pydantic import BaseModel


class FacebookDetail(BaseModel):
    username: str
    followers: Optional[str]
    city_1: Optional[int]
    city_pc_1: Optional[int]
    city_2: Optional[int]
    city_pc_2: Optional[int]
    city_3: Optional[int]
    city_pc_3: Optional[int]
    avg_views: Optional[str]
    max_views: Optional[str]
    min_views: Optional[str]
    consistency_score: Optional[int]
    avg_likes: Optional[str]
    avg_comments: Optional[str]
    avg_shares: Optional[str]
    engagement_rate: Optional[int]
