from typing import Optional

from pydantic import BaseModel


class FacebookDetail(BaseModel):
    id: Optional[str]
    username: Optional[str]
    followers: Optional[int]
    city_1: Optional[int]
    city_pc_1: Optional[int]
    city_2: Optional[int]
    city_pc_2: Optional[int]
    city_3: Optional[int]
    city_pc_3: Optional[int]
    avg_views: Optional[int]
    max_views: Optional[int]
    min_views: Optional[int]
    spread: Optional[int]
    avg_likes: Optional[int]
    avg_comments: Optional[int]
    avg_shares: Optional[int]
    engagement_rate: Optional[int]
