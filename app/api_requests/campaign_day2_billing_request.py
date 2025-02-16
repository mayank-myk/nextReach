from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.enums.payment_status import PaymentStatus


class CampaignDay2BillingRequest(BaseModel):
    day2_billing_date: date
    views: int
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
