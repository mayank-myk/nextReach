from pydantic import BaseModel, Field


class CollabRequest(BaseModel):
    user_id: int = Field(...)
    influencer_id: int = Field(...)
