from pydantic import BaseModel


class SuccessStoryResponse(BaseModel):
    id: int
    created_at: str
    title: str
    url: str
    category: str
    tag1: str
    tag2: str
    business_image: str
    influencer_image: str
