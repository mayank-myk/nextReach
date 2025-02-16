from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.enums.payment_status import PaymentStatus


class CampaignDay2PaymentRequest(BaseModel):
    payment_time: Optional[datetime] = None
    payment_status: PaymentStatus
