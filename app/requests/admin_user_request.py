from pydantic import BaseModel, Field

from app.enums.admin_type import AdminType


class AdminUserRequest(BaseModel):
    created_by: str = Field(min_length=1, max_length=255)
    admin_id: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=3, max_length=255)
    admin_type: AdminType
