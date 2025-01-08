from typing import Optional

from pydantic import BaseModel

from app.response.influencer.city_distribution_graph import CityDistributionGraph


class FacebookDetail(BaseModel):
    username: str
    followers: Optional[str]
    city_graph: Optional[CityDistributionGraph]
    avg_views: Optional[str]
    max_views: Optional[str]
    min_views: Optional[str]
    consistency_score: Optional[int]
    avg_likes: Optional[str]
    avg_comments: Optional[str]
    avg_shares: Optional[str]
    engagement_rate: Optional[int]
