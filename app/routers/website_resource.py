from typing import Optional, List

from fastapi import APIRouter, Query, Depends

from app.database.session import DatabaseSessionManager
from app.enums.average_view import AverageView
from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.content_price import ContentPrice
from app.enums.engagement_rate import EngagementRate
from app.enums.follower_count import FollowerCount
from app.enums.gender import Gender
from app.enums.influencer_age import InfluencerAge
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform
from app.enums.rating import Rating
from app.enums.reach_price import ReachPrice
from app.enums.sort_applied import SortApplied
from app.api_requests.influencer_insights import InfluencerInsights
from app.api_requests.waitlist_request import WaitListRequest
from app.response.generic_response import GenericResponse
from app.response.influencer_detail import InfluencerDetail
from app.response.influencer_listing import InfluencerListing
from app.services.web_service import WebService
from app.utils.logger import configure_logger

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
        user_id: int,
        page_number: int = Query(1, description="Page number to fetch", ge=1),
        page_size: int = Query(40, description="Number of influencers per page", ge=1, le=100),
        sort_applied: Optional[SortApplied] = Query(None, description="Sorting applied"),
        niche: Optional[List[Niche]] = Query(None, description="Influencer's niche"),
        city: Optional[List[City]] = Query(None, description="Region where influencer is located"),
        reach_price: Optional[List[ReachPrice]] = Query(None, description="Reach price"),
        follower_count: Optional[List[FollowerCount]] = Query(None, description="Minimum number of followers"),
        avg_views: Optional[List[AverageView]] = Query(None, description="Average views"),
        engagement: Optional[List[EngagementRate]] = Query(None, description="Engagement rate"),
        platform: Optional[Platform] = Query(None, description="Platform like Instagram, YouTube, etc."),
        content_price: Optional[ContentPrice] = Query(None, description="Content price"),
        collab_type: Optional[CollabType] = Query(None, description="Select one of the collab type"),
        gender: Optional[List[Gender]] = Query(None, description="Gender of the influencer"),
        age: Optional[List[InfluencerAge]] = Query(None, description="Age of the influencer"),
        rating: Optional[Rating] = Query(None, description="Minimum rating"),
        languages: Optional[List[Language]] = Query(None, description="Language"),
        db=Depends(db_manager.get_db)) -> InfluencerListing:
    web_service = WebService(db)
    return web_service.get_influencer_listing(user_id, page_number, page_size, sort_applied, niche, city, reach_price,
                                              follower_count, avg_views, engagement, platform, content_price, collab_type, gender,
                                              age, rating, languages)


@router.post('/influencer/insight')
def get_influencer_insight(request: InfluencerInsights, db=Depends(db_manager.get_db)) -> InfluencerDetail:
    web_service = WebService(db)
    return web_service.get_influencer_insight(request=request)


@router.post("/create/lead")
def create_lead(request: WaitListRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    web_service = WebService(db)
    return web_service.create_lead(request=request)
