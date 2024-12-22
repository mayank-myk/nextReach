from typing import Optional

from pydantic import BaseModel, Field

from app.models.entity_type import EntityType
from app.models.status import Status


class WaitListRequest(BaseModel):
    entity_type: EntityType
    name: str = Field(max_length=255)
    phone_number: str = Field(min_length=10, max_length=10)
    email: Optional[str] = Field(None, max_length=255)
    social_media_handle: Optional[str] = Field(None, max_length=255)
    message: Optional[str] = Field(None, max_length=1000)
    onboarding_status: Status = Status.PROCESSING
