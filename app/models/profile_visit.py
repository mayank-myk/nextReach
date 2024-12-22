from datetime import datetime
from pydantic import BaseModel, Field


class ProfileVisit(BaseModel):
    created_at: datetime.datetime
    influencer_id: str = Field(min_length=13, max_length=13, frozen=True)
    client_id: str = Field(min_length=13, max_length=13, frozen=True)
