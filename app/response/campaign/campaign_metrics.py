from pydantic import BaseModel


class CampaignMetrics(BaseModel):
    views: int
    likes: int
    comments: int
    shares: int
