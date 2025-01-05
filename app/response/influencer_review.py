from typing import List

from pydantic import BaseModel

from app.response.campaign_review import CampaignReview


class InfluencerReview(BaseModel):
    count: int
    avg_rating: int
    campaign_reviews: List[CampaignReview]

