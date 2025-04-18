from typing import List, Optional

from pydantic import BaseModel

from app.enums.sort_applied import SortApplied
from app.response.influencer_basic_detail import InfluencerBasicDetail
from app.response.search_filter import SearchFilter


class InfluencerListing(BaseModel):
    client_id: Optional[int] = None
    coin_balance: Optional[str] = None
    matched_influencer_list: List[InfluencerBasicDetail]
    unmatched_influencer_list: List[InfluencerBasicDetail]
    filters_applied: SearchFilter
    sorting_applied: Optional[SortApplied]
    page_number: int
    page_size: int
    result_start_number: int
    result_end_number: int
    result_total_count: int
    result_count_further_page: int
