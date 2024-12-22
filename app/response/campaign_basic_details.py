import datetime

from pydantic import BaseModel, Field

from app.models.campaign_stage import CampaignStage
from app.models.city import City
from app.models.niche import Niche
from app.models.status import Status


class CampaignBasicDetails(BaseModel):
    id: str = Field(min_length=13, max_length=13)
    created_at: datetime.datetime
    influencer_id: str = Field(min_length=13, max_length=13)
    influencer_image: str
    niche: Niche
    city: City
    stage: CampaignStage
    status: Status
