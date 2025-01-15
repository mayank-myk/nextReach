from pydantic import BaseModel, Field


class SuccessStoryRequest(BaseModel):
    title: str = Field(..., max_length=255)
    group_name: str = Field(..., max_length=255)
    url: str = Field(..., max_length=255)
    tag1: str = Field(..., max_length=255)
    tag2: str = Field(..., max_length=255)
    business_image: str = Field(..., max_length=255)
    influencer_image: str = Field(..., max_length=255)
