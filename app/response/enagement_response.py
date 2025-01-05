from pydantic import BaseModel


class EnagementMetric(BaseModel):
    engagement_rate: float
    engagement_quality: str
    followers: int
    likes: int
    comments: int
