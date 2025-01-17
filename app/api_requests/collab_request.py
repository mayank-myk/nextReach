from pydantic import BaseModel, Field


class CollabRequest(BaseModel):
    client_id: int = Field(...)
    influencer_id: int = Field(...)
