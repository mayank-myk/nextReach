import datetime

from pydantic import BaseModel

from app.models.status import Status


class BillingInfo(BaseModel):
    billing_amount: int
    billing_payment_at: datetime.datetime
    billing_payment_status: Status
