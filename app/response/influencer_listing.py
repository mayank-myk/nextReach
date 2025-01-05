from typing import List, Optional

from pydantic import BaseModel

from app.enums.sort_applied import SortApplied
from app.response.influencer_basic_detail import InfluencerBasicDetail
from app.response.search_filter import SearchFilter


class InfluencerListing(BaseModel):
    user_id: int
    coin_balance: int
    matched_influencer_list: List[InfluencerBasicDetail]
    unmatched_influencer_list: List[InfluencerBasicDetail]
    filters_applied: SearchFilter
    sorting_applied: Optional[SortApplied]
    page_number: int
    page_size: int
    total_match_number: int
