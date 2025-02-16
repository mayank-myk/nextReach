from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.enums.payment_status import PaymentStatus


class CampaignDay8PaymentRequest(BaseModel):
    payment_time: Optional[datetime] = None
    payment_status: PaymentStatus
    insight_1: Optional[str] = None
    insight_2: Optional[str] = None
    insight_3: Optional[str] = None
    insight_4: Optional[str] = None
    insight_5: Optional[str] = None
    insight_6: Optional[str] = None
