from typing import Optional

from pydantic import BaseModel

from app.enums.admin_type import AdminType


class LoginResponse(BaseModel):
    client_id: Optional[int] = None
    success: bool
    button_text: Optional[str] = "OKAY"
    message: Optional[str] = None
    admin_type: Optional[AdminType] = None
