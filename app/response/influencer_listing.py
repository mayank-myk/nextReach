from typing import List

from pydantic import BaseModel, Field

from app.response.influencer_detail import InfluencerDetail
from app.response.search_filter import SearchFilter


class InfluencerListing(BaseModel):
    user_id: str = Field(min_length=13, max_length=13)
    coin_balance: int
    influencer_details: List[InfluencerDetail]
    filters_applied: SearchFilter
    page_number: int
    quantity: int
