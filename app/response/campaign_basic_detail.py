from pydantic import BaseModel

from app.enums.status import Status
from app.response.influencer_basic_detail import InfluencerBasicDetail


class CampaignBasicDetail(BaseModel):
    id: int
    last_updated_at: str
    influencer_basic_detail: InfluencerBasicDetail
    status: Status
