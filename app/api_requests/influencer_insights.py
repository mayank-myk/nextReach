from typing import Optional

from pydantic import BaseModel, Field


class InfluencerInsights(BaseModel):
    client_id: Optional[int] = None
    influencer_id: int = Field(...)
