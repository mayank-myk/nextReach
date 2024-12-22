from typing import List

from app.database.session import DatabaseSessionManager
from app.requests.rate_campaign import RateCampaign
from app.response.campaign_basic_detail import CampaignBasicDetail
from app.response.campaign_detail import CampaignDetail
from app.response.generic_response import GenericResponse
from app.response.login_response import LoginResponse
from app.response.user_profile import UserProfile
from app.requests.collab_request import CollabRequest
from app.requests.profile_update import ProfileUpdate
from app.requests.user_login_request import UserLogin
from app.response.influencer_detail import InfluencerDetail
from app.services.campaign_service import CampaignService
from app.services.user_service import UserService
from app.utils.logger import configure_logger
from fastapi import APIRouter, Depends

_log = configure_logger()

router = APIRouter(
    prefix='/v1/user',
    tags=['user']
)

db_manager = DatabaseSessionManager()


@router.get("/profile/get/{user_id}")
def get_user_profile(user_id: str, db=Depends(db_manager.get_db)) -> UserProfile | GenericResponse:
    user_service = UserService(db)
    return user_service.get_user_profile(user_id=user_id)


@router.post("/profile/update/{user_id}")
def update_user_profile(user_id: str, profile: ProfileUpdate, db=Depends(db_manager.get_db)) -> GenericResponse:
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
def get_watchlist(user_id: str, db=Depends(db_manager.get_db)) -> List[InfluencerDetail]:
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
def get_user_campaign_all(user_id: str, db=Depends(db_manager.get_db)) -> List[CampaignBasicDetail] | GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.get_user_campaign_all(user_id=user_id)


@router.get("/campaign/detail/{campaign_id}")
def get_user_campaign_detail(campaign_id: str, db=Depends(db_manager.get_db)) -> CampaignDetail | GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.get_user_campaign_detail(campaign_id=campaign_id)


@router.post("/campaign/rate")
def rate_campaign(rate_campaign_request: RateCampaign, db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.rate_campaign(request=rate_campaign_request)
