from typing import Optional

from pydantic import BaseModel

from app.enums.response_action import ResponseAction


class GenericResponse(BaseModel):
    success: bool
    button_text: Optional[str] = "Okay"
    header: Optional[str] = "Oops"
    message: Optional[str] = None
    action: ResponseAction = ResponseAction.NO_ACTION
