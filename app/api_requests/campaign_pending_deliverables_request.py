from typing import Optional

from pydantic import BaseModel


class CampaignPendingDeliverables(BaseModel):
    deliverable_1: Optional[str] = None
    deliverable_2: Optional[str] = None
    deliverable_3: Optional[str] = None
    deliverable_4: Optional[str] = None
    deliverable_5: Optional[str] = None
    deliverable_6: Optional[str] = None
