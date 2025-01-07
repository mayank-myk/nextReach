from typing import Optional

from pydantic import BaseModel


class CampaignMetrics(BaseModel):
    views: Optional[str] = None
    likes: Optional[str] = None
    comments: Optional[str] = None
    shares: Optional[str] = None
