from typing import Optional

from pydantic import BaseModel, Field


class RateCampaign(BaseModel):
    user_id: str = Field(min_length=13, max_length=13)
    campaign_id: str = Field(min_length=13, max_length=13)
    rating: int = Field(ge=1, le=5)
    comment: Optional[str]
