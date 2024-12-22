import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.status import Status


class BillingInfo(BaseModel):
    billing_amount: Optional[int] = None
    billing_payment_at: Optional[datetime.datetime] = None
    billing_payment_status: Optional[Status] = None
