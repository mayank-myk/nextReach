from typing import Optional

from pydantic import BaseModel


class GenericResponse(BaseModel):
    success: bool
    button_text: Optional[str] = "OKAY"
    message: Optional[str] = None
