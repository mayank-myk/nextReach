from pydantic import BaseModel, Field


class CreateCollab(BaseModel):
    created_by: str = Field(..., min_length=3, max_length=255)
    client_id: int = Field(...)
    influencer_id: int = Field(...)
