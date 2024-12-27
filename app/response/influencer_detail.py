import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.gender import Gender
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform
from app.response.influencer_collab_charge import InfluencerCollabCharge
from app.response.influencer_metric_detail import InfluencerMetricDetail


class InfluencerDetail(BaseModel):
    id: str
    last_updated_at: datetime.datetime
    collaboration_request_raised: bool
    primary_platform: Platform
    name: str
    gender: Gender
    profile_picture: str
    languages: List[Language] = None
    next_reach_score: int
    niche: Niche
    city: City
    collab_type: CollabType
    deliverables: Optional[List[str]] = None
    content_charge: int
    views_charge: int
    collab_charge: InfluencerCollabCharge
    platform_details: InfluencerMetricDetail
