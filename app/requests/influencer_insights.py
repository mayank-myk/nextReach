from pydantic import BaseModel, Field


class InfluencerInsights(BaseModel):
    user_id: str = Field(min_length=13, max_length=13)
    influencer_id: str = Field(min_length=13, max_length=13)
