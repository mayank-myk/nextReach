from typing import Optional

from pydantic import BaseModel


class CampaignMetrics(BaseModel):
    views: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
