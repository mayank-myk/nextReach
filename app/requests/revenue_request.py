from pydantic import BaseModel, Field
from datetime import date
from app.models.client_type import ClientType
from app.models.revenue_type import RevenueType


class RevenueRequest(BaseModel):
    created_by: str = Field(min_length=5, max_length=255)
    date: date
    amount: int = Field(ge=1)
    description: str = Field(min_length=5, max_length=255)
    mode_of_payment: str = Field(min_length=5, max_length=255)
    account_id: str = Field(min_length=5, max_length=255)
    campaign_id: str = Field(min_length=13, max_length=13)
    paid_by: ClientType
    type: RevenueType
