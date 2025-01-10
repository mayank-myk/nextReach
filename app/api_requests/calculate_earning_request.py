from pydantic import BaseModel, Field

from app.enums.niche import Niche


class CalculateEarningRequest(BaseModel):
    niche: Niche
    follower_count: int = Field(...)
    avg_views: int = Field(...)
    engagement_rate: float = Field(...)
