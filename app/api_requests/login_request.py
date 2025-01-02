from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    admin_id: str = Field(..., min_length=5)
    password: str = Field(..., min_length=5)
