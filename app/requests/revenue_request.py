from datetime import date

from pydantic import BaseModel, Field

from app.enums.client_type import ClientType
from app.enums.revenue_type import RevenueType


class RevenueRequest(BaseModel):
    created_by: str = Field(..., min_length=5, max_length=255)  # Mandatory, with length constraints
    date: date  # Mandatory date
    amount: int = Field(..., ge=1)  # Mandatory integer with a minimum value of 1
    description: str = Field(..., min_length=5, max_length=255)  # Mandatory string with length constraints
    mode_of_payment: str = Field(..., min_length=5, max_length=255)  # Mandatory string with length constraints
    account_id: str = Field(..., min_length=5, max_length=255)  # Mandatory string with length constraints
    campaign_id: str = Field(..., min_length=13, max_length=13)  # Mandatory string with exact length constraint
    paid_by: ClientType  # Mandatory ClientType Enum
    type: RevenueType  # Mandatory RevenueType Enum
