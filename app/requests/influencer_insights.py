from pydantic import BaseModel, Field


class InfluencerInsights(BaseModel):
    user_id: int = Field(...)
    influencer_id: int = Field(...)
