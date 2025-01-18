from typing import Optional

from pydantic import BaseModel


class WaitListDump(BaseModel):
    id: int
    status: str
    ageing_day: int
    entity_type: str
    created_at: str
    name: str
    phone_number: str
    email: Optional[str] = None
    social_media_handle: Optional[str]
    message: Optional[str] = None
