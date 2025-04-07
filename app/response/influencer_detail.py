from typing import List, Optional

from pydantic import BaseModel

from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.content_subject import ContentSubject
from app.enums.content_type import ContentType
from app.enums.gender import Gender
from app.enums.niche import Niche
from app.enums.platform import Platform
from app.response.influencer.influencer_collab_charge import InfluencerCollabCharge
from app.response.influencer.influencer_metric_detail import InfluencerMetricDetail
from app.response.influencer.influencer_review import InfluencerReview


class InfluencerDetail(BaseModel):
    id: int
    last_updated_at: str
    collaboration_ongoing: bool
    primary_platform: Platform
    name: str
    gender: Optional[Gender] = None
    profile_picture: str
    languages: List[str] = None
    next_reach_score: int
    niche: List[Niche]
    blue_tick: bool = False
    city: City
    content_type: Optional[ContentType] = None
    content_subject: Optional[ContentSubject] = None
    collab_type: Optional[CollabType] = None
    deliverables: Optional[List[str]] = None
    content_charge: str
    views_charge: str
    fixed_charge: Optional[str] = None
    collab_charge: Optional[InfluencerCollabCharge] = None
    platform_details: InfluencerMetricDetail
    influencer_review: Optional[InfluencerReview] = None
    insights: Optional[List[str]] = None
