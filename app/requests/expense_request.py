from pydantic import BaseModel, Field
from datetime import date
from app.models.expense_type import ExpenseType


class ExpenseRequest(BaseModel):
    created_by: str = Field(min_length=5, max_length=255)
    type: ExpenseType
    date: date
    amount: int = Field(ge=1)
    description: str = Field(min_length=5, max_length=255)
    mode_of_payment: str = Field(min_length=5, max_length=255)
    account_id: str = Field(min_length=5, max_length=255)
