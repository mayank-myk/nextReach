from typing import Optional

from pydantic import BaseModel


class CampaignReview(BaseModel):
    user_name: Optional[str] = None
    rating: int
    comment: Optional[str] = None
    review_date: Optional[str] = None
