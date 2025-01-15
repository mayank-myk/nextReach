from pydantic import BaseModel


class AcademyVideoResponse(BaseModel):
    id: int
    created_at: str
    title: str
    yt_link: str
    category: str
    tag1: str
    tag2: str
    tag3: str
    tag4: str
