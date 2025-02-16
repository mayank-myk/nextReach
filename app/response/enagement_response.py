from typing import Optional

from pydantic import BaseModel


class EnagementMetric(BaseModel):
    engagement_rate: float
    engagement_quality: str
    followers: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
