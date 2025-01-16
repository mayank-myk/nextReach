from pydantic import BaseModel


class BlogResponse(BaseModel):
    id: int
    created_at: str
    author: str
    url: str
    title: str
    category: str
    blog_image: str
