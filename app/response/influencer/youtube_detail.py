from typing import Optional, List, Dict

from pydantic import BaseModel


class YouTubeDetail(BaseModel):
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

    city_graph: Optional[List[Dict]]
    age_graph: Optional[List[Dict]]
    sex_graph: Optional[List[Dict]]
