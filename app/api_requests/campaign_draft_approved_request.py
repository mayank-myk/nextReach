from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.enums.payment_status import PaymentStatus


class CampaignDraftApprovedRequest(BaseModel):
    content_draft_date: date
    billed_amount: int
    payment_time: Optional[datetime] = None
    payment_status: PaymentStatus
