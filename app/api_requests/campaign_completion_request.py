from typing import Optional

from pydantic import BaseModel


class CampaignCompletionRequest(BaseModel):
    insight_1: Optional[str] = None
    insight_2: Optional[str] = None
    insight_3: Optional[str] = None
    insight_4: Optional[str] = None
    insight_5: Optional[str] = None
    insight_6: Optional[str] = None
