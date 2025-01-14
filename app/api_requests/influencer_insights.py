from pydantic import BaseModel, Field


class InfluencerInsights(BaseModel):
    client_id: int = Field(...)
    influencer_id: int = Field(...)
