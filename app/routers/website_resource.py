from typing import Optional, List

from app.database.session import DatabaseSessionManager
from app.models.city import City
from app.models.gender import Gender
from app.requests.waitlist_request import WaitListRequest
from app.response.generic_response import GenericResponse
from app.models.niche import Niche
from app.models.platform import Platform
from app.requests.influencer_insights import InfluencerInsights
from app.response.influencer_detail import InfluencerDetail
from app.services.web_service import WebService
from app.utils.logger import configure_logger
from fastapi import APIRouter, Query, Depends

_log = configure_logger()

router = APIRouter(
    prefix='/v1/web',
    tags=['website']
)

db_manager = DatabaseSessionManager()


@router.get('/home/metadata')
def get_web_metadata(db=Depends(db_manager.get_db)) -> GenericResponse:
    web_service = WebService(db)
    return web_service.get_web_metadata()


@router.get('/influencer/discover/{user_id}')
def get_influencer_listings(
        user_id: str,
        page_number: int = Query(1, description="Page number to fetch", ge=1),
        page_size: int = Query(40, description="Number of influencers per page", ge=1, le=100),
        platform: Optional[Platform] = Query(None, description="Platform like Instagram, YouTube, etc."),
        content_price: Optional[List[int]] = Query(None, description="content price"),
        reach_price: Optional[List[int]] = Query(None, description="reach price"),
        niche: Optional[List[Niche]] = Query(None, description="Influencer's niche"),
        gender: Optional[List[Gender]] = Query(None, description="Gender of the influencer"),
        age: Optional[List[int]] = Query(None, description="Age of the influencer"),
        city: Optional[List[City]] = Query(None, description="Region where influencer is located"),
        rating: Optional[int] = Query(None, description="Minimum rating"),
        followers: Optional[List[int]] = Query(None, description="Minimum number of followers"),
        avg_views: Optional[List[int]] = Query(None, description="Average views"),
        engagement: Optional[int] = Query(None, description="Engagement rate"),
        consistency: Optional[int] = Query(None, description="Consistency score"),
        score: Optional[int] = Query(None, description="Overall score"),
        db=Depends(db_manager.get_db)) -> GenericResponse:
    web_service = WebService(db)
    return web_service.get_influencer_listing(user_id, page_number, page_size, platform, content_price, reach_price,
                                              niche, gender, age,
                                              city, rating, followers, avg_views, engagement, consistency, score)


@router.post('/influencer/insight')
def get_influencer_insight(request: InfluencerInsights, db=Depends(db_manager.get_db)) -> InfluencerDetail:
    web_service = WebService(db)
    return web_service.get_influencer_insight(request=request)


@router.post("/create/signup")
def create_lead(request: WaitListRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    web_service = WebService(db)
    return web_service.create_lead(request=request)
