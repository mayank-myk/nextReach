from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.enums.payment_status import PaymentStatus


class CampaignDay8BillingRequest(BaseModel):
    day8_billing_date: date
    billed_amount: int
    payment_time: datetime
    payment_status: PaymentStatus
    views: int
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
