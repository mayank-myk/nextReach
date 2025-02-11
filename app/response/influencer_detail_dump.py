from typing import List, Optional

from pydantic import BaseModel


class InfluencerDetailDump(BaseModel):
    id: int
    last_updated_at: str
    primary_platform: str
    name: str
    phone_number: str
    email: Optional[str] = None
    content_charge: int
    views_charge: int
    niche: List[str]
    gender: Optional[str] = None
    languages: List[str] = None
    next_reach_score: int
    city: str
    profile_picture: str
    collab_type: str
    deliverables: Optional[List[str]] = None
