from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=10, frozen=True)
    otp: str = Field(..., min_length=5, max_length=5, frozen=True)
