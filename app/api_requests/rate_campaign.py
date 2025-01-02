from typing import Optional

from pydantic import BaseModel, Field


class RateCampaign(BaseModel):
    user_id: int = Field(...)
    campaign_id: int = Field(...)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)
