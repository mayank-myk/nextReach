from typing import Optional

from pydantic import BaseModel

from app.response.campaign.billing_info import BillingInfo


class ContentDraft(BaseModel):
    date: Optional[str] = None
    billing_info: BillingInfo
