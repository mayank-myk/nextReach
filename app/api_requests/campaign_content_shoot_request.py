from datetime import date

from pydantic import BaseModel


class CampaignContentShootRequest(BaseModel):
    content_shoot_date: date
