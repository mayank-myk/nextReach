import datetime

from pydantic import BaseModel, Field

from app.models.campaign_stage import CampaignStage
from app.models.status import Status
from app.response.campaign.influencer_basic_detail import InfluencerBasicDetail


class CampaignBasicDetails(BaseModel):
    id: str = Field(min_length=13, max_length=13)
    created_at: datetime.datetime
    influencer_basic_detail: InfluencerBasicDetail
    stage: CampaignStage
    status: Status
