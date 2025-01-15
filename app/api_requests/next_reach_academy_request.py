from pydantic import BaseModel, Field


class NextReachAcademyRequest(BaseModel):
    yt_link: str = Field(..., max_length=1000)
    title: str = Field(..., max_length=255)
    category: str = Field(..., max_length=255)
    tag1: str = Field(..., max_length=255)
    tag2: str = Field(..., max_length=255)
    tag3: str = Field(..., max_length=255)
    tag4: str = Field(..., max_length=255)
