import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.models.campaign_stage import CampaignStage
from app.models.content_type import ContentType
from app.response.campaign.campaign_billing import CampaignBilling
from app.response.campaign.content_post import ContentPost
from app.response.campaign.influencer_basic_detail import InfluencerBasicDetail


class CampaignDetail(BaseModel):
    id: str
    last_updated_at: datetime.datetime
    campaign_managed_by: str
    influencer_basic_detail: InfluencerBasicDetail
    stage: CampaignStage
    content_charge: int
    views_charge: int
    type_of_content: Optional[ContentType]= None
    rating: Optional[int] = None
    review: Optional[str] = None
    influencer_finalization_date: Optional[datetime.datetime] = None
    content_shoot_date: Optional[datetime.datetime] = None
    content_post: Optional[ContentPost] = None
    first_billing: Optional[CampaignBilling] = None
    second_billing: Optional[CampaignBilling] = None
    post_insights: Optional[List[str]] = None
    pending_deliverables: Optional[List[str]] = None
