from typing import List

from pydantic import BaseModel, Field

from app.models.city import City
from app.models.gender import Gender
from app.models.niche import Niche
from app.models.platform import Platform


class SearchFilter(BaseModel):
    platform: Platform
    content_price: List[int]
    reach_price: List[int]
    niche: List[Niche]
    gender: List[Gender]
    age: List[int]
    city: List[City]
    followers: List[int]
    avg_views: List[int]
    rating: int
    engagement: int
    consistency: int
    score: int
