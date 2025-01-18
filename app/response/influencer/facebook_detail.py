from typing import Optional

from pydantic import BaseModel

from app.response.influencer.age_distribution_graph import AgeDistributionGraph
from app.response.influencer.city_distribution_graph import CityDistributionGraph
from app.response.influencer.sex_distribution_graph import SexDistributionGraph


class FacebookDetail(BaseModel):
    id: int
    username: str
    followers: Optional[str]
    avg_views: Optional[str]
    max_views: Optional[str]
    min_views: Optional[str]
    consistency_score: Optional[int]
    avg_likes: Optional[str]
    avg_comments: Optional[str]
    avg_shares: Optional[str]
    engagement_rate: Optional[int]

    city_graph: Optional[CityDistributionGraph]
    age_graph: Optional[AgeDistributionGraph]
    sex_graph: Optional[SexDistributionGraph]
