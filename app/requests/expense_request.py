from datetime import date

from pydantic import BaseModel, Field

from app.enums.expense_type import ExpenseType


class ExpenseRequest(BaseModel):
    created_by: str = Field(..., min_length=1, max_length=255)
    type: ExpenseType
    date: date
    amount: int = Field(..., ge=1)  # Mandatory integer with a minimum value of 1
    description: str = Field(..., min_length=1, max_length=255)  # Mandatory string with length constraints
    mode_of_payment: str = Field(..., min_length=1, max_length=255)  # Mandatory string with length constraints
    account_id: str = Field(..., min_length=1, max_length=255)  # Mandatory string with length constraints
