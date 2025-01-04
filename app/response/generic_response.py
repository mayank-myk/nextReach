from typing import Optional

from pydantic import BaseModel


class GenericResponse(BaseModel):
    success: bool
    button_text: Optional[str] = "Okay"
    header: Optional[str] = "Oops"
    message: Optional[str] = None
