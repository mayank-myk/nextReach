import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.campaign_stage import CampaignStage
from app.models.content_type import ContentType
from app.response.campaign.campaign_billing import CampaignBilling
from app.response.campaign.content_post import ContentPost
from app.response.campaign.influencer_basic_detail import InfluencerBasicDetail


class CampaignDetail(BaseModel):
    id: str = Field(min_length=13, max_length=13)
    last_updated_at: datetime.datetime
    campaign_managed_by: str = Field(min_length=5, frozen=True)
    influencer_basic_detail: InfluencerBasicDetail
    stage: CampaignStage
    content_charge: int = Field(ge=0, frozen=True)
    views_charge: int = Field(ge=0, frozen=True)
    type_of_content: ContentType
    campaign_notes: str = Field(min_length=5)
    rating: int
    review: str
    influencer_finalization_date: Optional[datetime]
    content_shoot_date: Optional[datetime]
    content_post: ContentPost
    first_billing: CampaignBilling
    second_billing: CampaignBilling
    post_insights: List[str]
    pending_deliverables: List[str]
