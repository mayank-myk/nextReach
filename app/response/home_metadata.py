from typing import List

from pydantic import BaseModel

from app.response.academy_video_response import AcademyVideoResponse
from app.response.blog_response import BlogResponse
from app.response.influencer_basic_detail import InfluencerBasicDetail
from app.response.success_story_response import SuccessStoryResponse


class HomeMetadata(BaseModel):
    academy_video_list: List[AcademyVideoResponse]
    success_story_list: List[SuccessStoryResponse]
    blog_list: List[BlogResponse]
    influencer_list: List[InfluencerBasicDetail]
