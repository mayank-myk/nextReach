from typing import Optional

from pydantic import BaseModel, Field


class RateCampaign(BaseModel):
    user_id: str = Field(...)
    campaign_id: str = Field(...)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)
