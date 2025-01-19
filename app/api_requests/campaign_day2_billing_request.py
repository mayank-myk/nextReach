from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.enums.payment_status import PaymentStatus


class CampaignDay2BillingRequest(BaseModel):
    day2_billing_date: date
    billed_amount: int
    payment_time: Optional[datetime] = None
    payment_status: PaymentStatus
    views: int
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
