import datetime

from pydantic import BaseModel

from app.enums.campaign_stage import CampaignStage
from app.enums.status import Status
from app.response.influencer_basic_detail import InfluencerBasicDetail


class CampaignBasicDetail(BaseModel):
    id: str
    created_at: datetime.datetime
    influencer_basic_detail: InfluencerBasicDetail
    stage: CampaignStage
    status: Status
