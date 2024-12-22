from pydantic import BaseModel


class GenericResponse(BaseModel):
    success: bool
    error_code: int
    error_message: str
