from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi import Query

from app.api_requests.collab_request import CollabRequest
from app.api_requests.influencer_insights import InfluencerInsights
from app.api_requests.profile_update import ProfileUpdate
from app.api_requests.rate_campaign import RateCampaign
from app.api_requests.user_login_request import UserLogin
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
from app.response.campaign_basic_detail import CampaignBasicDetail
from app.response.campaign_detail import CampaignDetail
from app.response.generic_response import GenericResponse
from app.response.influencer_detail import InfluencerDetail
from app.response.influencer_listing import InfluencerListing
from app.response.login_response import LoginResponse
from app.response.user_profile import UserProfile
from app.services.campaign_service import CampaignService
from app.services.user_service import UserService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/user',
    tags=['User Resources (Only For Website)']
)

db_manager = DatabaseSessionManager()


@router.get("/profile/get/{user_id}")
def get_user_profile(user_id: int, db=Depends(db_manager.get_db)) -> UserProfile | GenericResponse:
    user_service = UserService(db)
    return user_service.get_user_profile(user_id=user_id)


@router.post("/profile/update/{user_id}")
def update_user_profile(user_id: int, profile: ProfileUpdate, db=Depends(db_manager.get_db)) -> GenericResponse:
    user_service = UserService(db)
    return user_service.update_user_profile(user_id=user_id, profile=profile)


@router.get("/request/otp/{phone_number}")
def request_otp(phone_number: str, db=Depends(db_manager.get_db)) -> GenericResponse:
    user_service = UserService(db)
    return user_service.send_otp(phone_number=phone_number)


@router.post("/validate/otp")
def validate_otp(request: UserLogin, db=Depends(db_manager.get_db)) -> LoginResponse:
    user_service = UserService(db)
    return user_service.validate_otp(phone_number=request.phone_number, otp=request.otp)


@router.get("/watchlist/all/{user_id}")
def get_watchlist(user_id: int, db=Depends(db_manager.get_db)) -> List[InfluencerDetail]:
    user_service = UserService(db)
    return user_service.get_watchlist(user_id=user_id)


@router.post("/watchlist/add")
def add_to_watchlist(request: CollabRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    user_service = UserService(db)
    return user_service.add_to_watchlist(user_id=request.user_id, influencer_id=request.influencer_id)


@router.post("/watchlist/remove")
def remove_from_watchlist(request: CollabRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    user_service = UserService(db)
    return user_service.remove_from_watchlist(user_id=request.user_id, influencer_id=request.influencer_id)


@router.post("/request/collab")
def request_collab(request: CollabRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    user_service = UserService(db)
    return user_service.request_collab(user_id=request.user_id, influencer_id=request.influencer_id)


@router.get("/campaign/all/{user_id}")
def get_user_campaign_all(user_id: int, db=Depends(db_manager.get_db)) -> List[CampaignBasicDetail] | GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.get_user_campaign_all(user_id=user_id)


@router.get("/campaign/detail/{campaign_id}")
def get_user_campaign_detail(campaign_id: int, db=Depends(db_manager.get_db)) -> CampaignDetail | GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.get_user_campaign_detail(campaign_id=campaign_id)


@router.post("/campaign/rate")
def rate_campaign(rate_campaign_request: RateCampaign, db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.rate_campaign(request=rate_campaign_request)


@router.get('/influencer/discover/{user_id}')
def get_influencer_listings(
        user_id: int,
        page_number: int = Query(1, description="Page number to fetch", ge=1),
        page_size: int = Query(40, description="Number of influencers per page", ge=1, le=100),
        sort_applied: SortApplied = Query(SortApplied.RECOMMENDED, description="Sorting applied"),
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
    user_service = UserService(db)
    return user_service.get_influencer_listing(user_id, page_number, page_size, sort_applied, niche, city, reach_price,
                                               follower_count, avg_views, engagement, platform, content_price,
                                               collab_type, gender, age, rating, languages)


@router.post('/influencer/insight')
def get_influencer_insight(request: InfluencerInsights, db=Depends(db_manager.get_db)) -> InfluencerDetail:
    user_service = UserService(db)
    return user_service.get_influencer_insight(request=request)
