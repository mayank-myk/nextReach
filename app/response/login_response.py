from typing import Optional

from pydantic import BaseModel

from app.models.admin_type import AdminType


class LoginResponse(BaseModel):
    user_id: Optional[str] = None
    success: bool
    message: Optional[str] = None
    admin_type: Optional[AdminType] = None
