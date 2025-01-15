from typing import Optional, Dict, List

from fastapi import APIRouter, Depends

from app.api_requests.calculate_earning_request import CalculateEarningRequest
from app.api_requests.waitlist_request import WaitListRequest
from app.database.session import DatabaseSessionManager
from app.response.academy_video_response import AcademyVideoResponse
from app.response.blog_response import BlogResponse
from app.response.enagement_response import EnagementMetric
from app.response.generic_response import GenericResponse
from app.response.success_story_response import SuccessStoryResponse
from app.services.web_service import WebService, calculate_influencer_earning, calculate_engagement_rate
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/web',
    tags=['Website Resources (Only For Website)']
)

db_manager = DatabaseSessionManager()


@router.get('/home/metadata')
def get_web_metadata(db=Depends(db_manager.get_db)) -> GenericResponse:
    web_service = WebService(db)
    return web_service.get_web_metadata()


@router.post("/create/lead")
def create_lead(request: WaitListRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    web_service = WebService(db)
    return web_service.create_lead(request=request)


@router.post("/calculate/earning")
def influencer_earning(request: CalculateEarningRequest) -> str:
    return calculate_influencer_earning(request=request)


@router.get("/calculate/er/{insta_username}")
def engagement_rate(insta_username: str) -> EnagementMetric | GenericResponse:
    return calculate_engagement_rate(username=insta_username)


@router.get("/get/blog/{url}", response_model=None)
def get_blog_by_id(url: str, db=Depends(db_manager.get_db)) -> Optional[str]:
    web_service = WebService(db)
    return web_service.get_blog_by_url(url=url)


@router.get('/get/blog/all', response_model=None)
def get_all_blogs(db=Depends(db_manager.get_db)) -> Dict[str, List[BlogResponse]]:
    web_service = WebService(db)
    return web_service.get_all_blogs()


@router.get("/get/success-story/{url}", response_model=None)
def get_blog_by_url(url: str, db=Depends(db_manager.get_db)) -> Optional[str]:
    web_service = WebService(db)
    return web_service.get_ss_by_url(url=url)


@router.get('/get/success-story/all')
def get_all_ss(db=Depends(db_manager.get_db)) -> Dict[str, List[SuccessStoryResponse]]:
    web_service = WebService(db)
    return web_service.get_all_ss()


@router.get('/get/academy-video/all')
def get_all_nra(db=Depends(db_manager.get_db)) -> Dict[str, List[AcademyVideoResponse]]:
    web_service = WebService(db)
    return web_service.get_all_nra()
