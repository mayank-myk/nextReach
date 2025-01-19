from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from app.enums.content_type import ContentType


class CampaignInfluencerFinalizedRequest(BaseModel):
    campaign_managed_by: str = Field(..., max_length=255)
    type_of_content: Optional[ContentType] = None
    influencer_finalization_date: date
