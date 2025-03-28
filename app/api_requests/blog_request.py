from datetime import date

from pydantic import BaseModel, Field


class BlogRequest(BaseModel):
    author: str = Field(..., max_length=255, description="Name of the author")
    title: str = Field(..., max_length=255, description="Title of the blog")
    url: str = Field(..., max_length=255)
    category: str = Field(..., max_length=255, description="Category or group the blog belongs to")
    created_at: date = Field(..., description="Date when the blog is created. Defaults to today.")
    blog_image: str = Field(..., max_length=255, description="Category or group the blog belongs to")
