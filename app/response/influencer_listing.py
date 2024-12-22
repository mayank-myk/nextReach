from typing import List, Optional

from pydantic import BaseModel, Field

from app.enums.sort_applied import SortApplied
from app.response.influencer_basic_detail import InfluencerBasicDetail
from app.response.search_filter import SearchFilter


class InfluencerListing(BaseModel):
    user_id: str = Field(min_length=13, max_length=13)
    coin_balance: int
    influencer_list: List[InfluencerBasicDetail]
    filters_applied: SearchFilter
    sorting_applied: Optional[SortApplied]
    page_number: int
    page_size: int
    total_match_number: int
