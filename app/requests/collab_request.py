from pydantic import BaseModel, Field


class CollabRequest(BaseModel):
    user_id: str = Field(...)
    influencer_id: str = Field(...)
