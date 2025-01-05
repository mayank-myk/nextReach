from pydantic import BaseModel, Field


class CalculateErRequest(BaseModel):
    insta_username: str = Field(...)
