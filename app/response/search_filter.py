from typing import List, Optional

from pydantic import BaseModel

from app.enums.average_view import AverageView
from app.enums.budget import Budget
from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.content_price import ContentPrice
from app.enums.engagement_rate import EngagementRate
from app.enums.follower_count import FollowerCount
from app.enums.gender import Gender
from app.enums.influencer_age import InfluencerAge
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform
from app.enums.rating import Rating
from app.enums.reach_price import ReachPrice


class SearchFilter(BaseModel):
    niche: Optional[List[Niche]] = None
    city: Optional[List[City]] = None
    reach_price: Optional[List[ReachPrice]] = None
    follower_count: Optional[List[FollowerCount]] = None
    avg_views: Optional[List[AverageView]] = None
    engagement: Optional[EngagementRate] = None
    platform: Optional[Platform] = None
    budget: Optional[Budget] = None
    content_price: Optional[ContentPrice] = None
    gender: Optional[List[Gender]] = None
    collab_type: Optional[CollabType] = None
    age: Optional[List[InfluencerAge]] = None
    rating: Optional[Rating] = None
    languages: Optional[List[Language]] = None
