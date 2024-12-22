from typing import List, Optional

from pydantic import BaseModel

from app.enums.city import City
from app.enums.gender import Gender
from app.enums.niche import Niche
from app.enums.platform import Platform


class SearchFilter(BaseModel):
    platform: Optional[Platform] = None  # Optional field (Platform type)
    content_price: Optional[List[int]] = None  # Optional list of integers
    reach_price: Optional[List[int]] = None  # Optional list of integers
    niche: Optional[List[Niche]] = None  # Optional list of Niche items
    gender: Optional[List[Gender]] = None  # Optional list of Gender items
    age: Optional[List[int]] = None  # Optional list of integers
    city: Optional[List[City]] = None  # Optional list of City items
    followers: Optional[List[int]] = None  # Optional list of integers
    avg_views: Optional[List[int]] = None  # Optional list of integers
    rating: Optional[int] = None  # Optional integer field
    engagement: Optional[int] = None  # Optional integer field
    consistency: Optional[int] = None  # Optional integer field
    score: Optional[int] = None  # Optional integer field
