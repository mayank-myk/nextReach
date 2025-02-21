from typing import Optional

from pydantic import BaseModel, Field

from app.enums.collab_date import CollabDate


class CollabRequest(BaseModel):
    client_id: Optional[int] = None
    influencer_id: int = Field(...)
    collab_date: Optional[CollabDate] = None
