from fastapi import APIRouter, Depends

from app.api_requests.influencer_fb_metric_request import InfluencerFbMetricRequest
from app.api_requests.influencer_insta_metric_request import InfluencerInstaMetricRequest
from app.api_requests.influencer_yt_metric_request import InfluencerYtMetricRequest
from app.api_requests.update_influencer_fb_metric_request import UpdateInfluencerFbMetricRequest
from app.api_requests.update_influencer_insta_metric_request import UpdateInfluencerInstaMetricRequest
from app.api_requests.update_influencer_yt_metric_request import UpdateInfluencerYtMetricRequest
from app.database.influencer_fb_metric_table import InfluencerFbMetric
from app.database.influencer_insta_metric_table import InfluencerInstaMetric
from app.database.influencer_yt_metric_table import InfluencerYtMetric
from app.database.session import DatabaseSessionManager
from app.response.generic_response import GenericResponse
from app.services.influencer_service import InfluencerService
from app.utils.logger import configure_logger

_log = configure_logger()
ALLOWED_IMAGE_MIME_TYPES = ["image/jpeg", "image/png", "image/jpg"]
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

router = APIRouter(
    prefix='/v1/influencer/metric',
    tags=['Influencer Metric Resource (Only For Admins)']
)

db_manager = DatabaseSessionManager()


@router.post("/create/insta/{influencer_id}")
def create_influencer_insta_metric(influencer_id: int, request: InfluencerInstaMetricRequest,
                                   db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.create_influencer_insta_metric(influencer_id=influencer_id, request=request)


@router.post("/create/yt/{influencer_id}")
def create_influencer_yt_metric(influencer_id: int, request: InfluencerYtMetricRequest,
                                db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.create_influencer_yt_metric(influencer_id=influencer_id, request=request)


@router.post("/create/fb/{influencer_id}")
def create_influencer_fb_metric(influencer_id: int, request: InfluencerFbMetricRequest,
                                db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.create_influencer_fb_metric(influencer_id=influencer_id, request=request)


@router.post("/update/insta/{influencer_insta_metric_id}")
def update_influencer_insta_metric(influencer_insta_metric_id: int, request: UpdateInfluencerInstaMetricRequest,
                                   db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.update_influencer_insta_metric(influencer_insta_metric_id=influencer_insta_metric_id,
                                                             request=request)


@router.post("/update/yt/{influencer_yt_metric_id}")
def update_influencer_yt_metric(influencer_yt_metric_id: int, request: UpdateInfluencerYtMetricRequest,
                                db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.update_influencer_yt_metric(influencer_yt_metric_id=influencer_yt_metric_id,
                                                          request=request)


@router.post("/update/fb/{influencer_fb_metric_id}")
def update_influencer_fb_metric(influencer_fb_metric_id: int, request: UpdateInfluencerFbMetricRequest,
                                db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.update_influencer_fb_metric(influencer_fb_metric_id=influencer_fb_metric_id,
                                                          request=request)


@router.get("/get/insta/{influencer_id}", response_model=None)
def get_influencer_insta_latest_metric(influencer_id: int,
                                       db=Depends(db_manager.get_db)) -> InfluencerInstaMetric | GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.get_influencer_insta_metric_detail(influencer_id=influencer_id)


@router.get("/get/yt/{influencer_id}", response_model=None)
def get_influencer_yt_latest_metric(influencer_id: int,
                                    db=Depends(db_manager.get_db)) -> InfluencerYtMetric | GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.get_influencer_yt_metric_detail(influencer_id=influencer_id)


@router.get("/get/fb/{influencer_id}", response_model=None)
def get_influencer_fb_latest_metric(influencer_id: int,
                                    db=Depends(db_manager.get_db)) -> InfluencerFbMetric | GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.get_influencer_fb_metric_detail(influencer_id=influencer_id)
