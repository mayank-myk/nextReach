from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi import BackgroundTasks
from fastapi import Query

from app.api_requests.client_login_request import ClientLogin
from app.api_requests.collab_request import CollabRequest
from app.api_requests.influencer_insights import InfluencerInsights
from app.api_requests.profile_update import ProfileUpdate
from app.api_requests.rate_campaign import RateCampaign
from app.database.session import DatabaseSessionManager
from app.enums.average_view import AverageView
from app.enums.budget import Budget
from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.content_price import ContentPrice
from app.enums.engagement_rate import EngagementRate
from app.enums.follower_count import FollowerCount
from app.enums.gender import Gender
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform
from app.enums.rating import Rating
from app.enums.reach_price import ReachPrice
from app.enums.sort_applied import SortApplied
from app.response.campaign_basic_detail import CampaignBasicDetail
from app.response.campaign_detail import CampaignDetail
from app.response.client_profile import ClientProfile
from app.response.generic_response import GenericResponse
from app.response.influencer_detail import InfluencerDetail
from app.response.influencer_listing import InfluencerListing
from app.response.login_response import LoginResponse
from app.services.campaign_service import CampaignService
from app.services.client_service import ClientService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/web',
    tags=['Website Client Interaction (Only For Website)']
)

db_manager = DatabaseSessionManager()


@router.get("/profile/get/{client_id}")
def get_client_profile(client_id: int, db=Depends(db_manager.get_db)) -> ClientProfile | GenericResponse:
    client_service = ClientService(db)
    return client_service.get_client_profile(client_id=client_id)


@router.post("/profile/update/{client_id}")
def update_client_profile(client_id: int, profile: ProfileUpdate, db=Depends(db_manager.get_db)) -> GenericResponse:
    client_service = ClientService(db)
    return client_service.update_client_profile(client_id=client_id, profile=profile)


@router.get("/request/otp/{phone_number}")
def request_otp(background_tasks: BackgroundTasks, phone_number: str, db=Depends(db_manager.get_db)) -> GenericResponse:
    client_service = ClientService(db)
    return client_service.send_otp(phone_number=phone_number, background_tasks=background_tasks)


@router.post("/validate/otp")
def validate_otp(request: ClientLogin, db=Depends(db_manager.get_db)) -> LoginResponse:
    client_service = ClientService(db)
    return client_service.validate_otp(phone_number=request.phone_number, otp=request.otp)


@router.get("/watchlist/all/{client_id}")
def get_watchlist(client_id: int, db=Depends(db_manager.get_db)) -> List[InfluencerDetail]:
    client_service = ClientService(db)
    return client_service.get_watchlist(client_id=client_id)


@router.post("/watchlist/add")
def add_to_watchlist(request: CollabRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    client_service = ClientService(db)
    return client_service.add_to_watchlist(client_id=request.client_id, influencer_id=request.influencer_id)


@router.post("/watchlist/remove")
def remove_from_watchlist(request: CollabRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    client_service = ClientService(db)
    return client_service.remove_from_watchlist(client_id=request.client_id, influencer_id=request.influencer_id)


@router.post("/request/collab")
def request_collab(request: CollabRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    client_service = ClientService(db)
    return client_service.request_collab(created_by="client_id_" + str(request.client_id), client_id=request.client_id,
                                         influencer_id=request.influencer_id, collab_date=request.collab_date)


@router.get("/campaign/all/{client_id}")
def get_client_campaign_all(client_id: int, db=Depends(db_manager.get_db)) -> List[
                                                                                  CampaignBasicDetail] | GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.get_client_campaign_all(client_id=client_id)


@router.get("/campaign/detail/{campaign_id}")
def get_client_campaign_detail(campaign_id: int, db=Depends(db_manager.get_db)) -> CampaignDetail | GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.get_client_campaign_detail(campaign_id=campaign_id)


@router.post("/campaign/rate")
def rate_campaign(rate_campaign_request: RateCampaign, db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.rate_campaign(request=rate_campaign_request)


@router.get('/influencer/discover')
def get_influencer_listings(
        background_tasks: BackgroundTasks,
        client_id: int = Query(1, description="Client Id", ge=1),
        page_number: int = Query(1, description="Page number to fetch", ge=1),
        page_size: int = Query(40, description="Number of influencers per page", ge=1, le=100),
        sort_applied: SortApplied = Query(SortApplied.RECOMMENDED, description="Sorting applied"),
        niche: Optional[List[Niche]] = Query(None, description="Influencer's niche"),
        city: Optional[City] = Query(None, description="Region where influencer is located"),
        reach_price: Optional[List[ReachPrice]] = Query(None, description="Reach price"),
        follower_count: Optional[List[FollowerCount]] = Query(None, description="Minimum number of followers"),
        avg_views: Optional[List[AverageView]] = Query(None, description="Average views"),
        engagement: Optional[EngagementRate] = Query(None, description="Engagement rate"),
        platform: Optional[Platform] = Query(None, description="Platform like Instagram, YouTube, etc."),
        content_price: Optional[ContentPrice] = Query(None, description="Content price"),
        budget: Optional[Budget] = Query(None, description="Budget"),
        collab_type: Optional[CollabType] = Query(None, description="Select one of the collab type"),
        gender: Optional[Gender] = Query(None, description="Gender of the influencer"),
        rating: Optional[Rating] = Query(None, description="Minimum rating"),
        languages: Optional[List[Language]] = Query(None, description="Language"),
        db=Depends(db_manager.get_db)) -> InfluencerListing:
    client_service = ClientService(db)
    return client_service.get_influencer_listing(client_id, page_number, page_size, sort_applied, niche, city,
                                                 reach_price, follower_count, avg_views, engagement, platform, budget,
                                                 content_price, collab_type, gender, rating, languages,
                                                 background_tasks)


@router.post('/influencer/insight')
def get_influencer_insight(request: InfluencerInsights,
                           db=Depends(db_manager.get_db)) -> InfluencerDetail | GenericResponse:
    client_service = ClientService(db)
    return client_service.get_influencer_insight(request=request)
