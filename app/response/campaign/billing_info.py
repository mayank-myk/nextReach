from typing import Optional

from pydantic import BaseModel

from app.enums.payment_status import PaymentStatus


class BillingInfo(BaseModel):
    billing_amount: Optional[int] = None
    billing_payment_at: Optional[str] = None
    billing_payment_status: Optional[PaymentStatus] = None
