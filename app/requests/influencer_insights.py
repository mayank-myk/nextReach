from pydantic import BaseModel, Field


class InfluencerInsights(BaseModel):
    user_id: str = Field(...)
    influencer_id: str = Field(...)
