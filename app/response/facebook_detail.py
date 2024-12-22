from pydantic import BaseModel, Field


class FacebookDetail(BaseModel):
    id: str = Field(min_length=13, max_length=13, frozen=True)
    username: str = Field(min_length=5, max_length=100)
    followers: int = Field(ge=0)
    city_1: int = Field(ge=0)
    city_pc_1: int = Field(ge=0)
    city_2: int = Field(ge=0)
    city_pc_2: int = Field(ge=0)
    city_3: int = Field(ge=0)
    city_pc_3: int = Field(ge=0)
    avg_views: int = Field(ge=0)
    max_views: int = Field(ge=0)
    min_views: int = Field(ge=0)
    spread: int = Field(ge=0)
    avg_likes: int = Field(ge=0)
    avg_comments: int = Field(ge=0)
    avg_shares: int = Field(ge=0)
    engagement_rate: int = Field(ge=0)
