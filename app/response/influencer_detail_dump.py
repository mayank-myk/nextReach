from typing import List, Optional

from pydantic import BaseModel


class InfluencerDetailDump(BaseModel):
    influencer_id: int
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
    influencer_insta_metric_id: Optional[int] = None
    username: Optional[str] = None
    profile_link: Optional[str] = None
    consistency_score: Optional[int] = None
    engagement_rate: Optional[float] = None
    followers: Optional[int] = None
    avg_views: Optional[int] = None
    max_views: Optional[int] = None
    avg_likes: Optional[int] = None
    avg_comments: Optional[int] = None
    avg_shares: Optional[int] = None
    city_1: Optional[str] = None
    city_pc_1: Optional[int] = None
    city_2: Optional[str] = None
    city_pc_2: Optional[int] = None
    city_3: Optional[str] = None
    city_pc_3: Optional[int] = None
    age_13_to_17: Optional[int] = None
    age_18_to_24: Optional[int] = None
    age_25_to_34: Optional[int] = None
    age_35_to_44: Optional[int] = None
    age_45_to_54: Optional[int] = None
    age_55: Optional[int] = None
    men_follower_pc: Optional[int] = None
    women_follower_pc: Optional[int] = None