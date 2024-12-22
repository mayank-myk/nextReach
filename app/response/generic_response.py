from pydantic import BaseModel


class GenericResponse(BaseModel):
    user_id: str
    success: bool
    error_code: int
    error_message: str
