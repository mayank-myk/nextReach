import os

from fastapi import APIRouter, Depends, UploadFile, File

from app.api_requests.influencer_insights import InfluencerInsights
from app.api_requests.influencer_metric_request import InfluencerMetricRequest
from app.api_requests.influencer_request import InfluencerRequest
from app.api_requests.update_influencer_metric_request import UpdateInfluencerMetricRequest
from app.api_requests.update_influencer_request import UpdateInfluencerRequest
from app.database.influencer_metric_table import InfluencerMetric
from app.database.influencer_table import Influencer
from app.database.session import DatabaseSessionManager
from app.response.generic_response import GenericResponse
from app.response.influencer_detail import InfluencerDetail
from app.services.influencer_service import InfluencerService
from app.services.user_service import UserService
from app.utils.logger import configure_logger

_log = configure_logger()
ALLOWED_IMAGE_MIME_TYPES = ["image/jpeg", "image/png", "image/jpg"]
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

router = APIRouter(
    prefix='/v1/influencer',
    tags=['Create/Update Influencer (Only For Admins)']
)

db_manager = DatabaseSessionManager()


@router.post("/create")
def create_influencer(request: InfluencerRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.create_influencer(request=request)


@router.post("/upload/image/{influencer_id}")
def create_influencer(influencer_id: int, image_file: UploadFile = File(...),
                      db=Depends(db_manager.get_db)) -> GenericResponse:
    if image_file.content_type not in ALLOWED_IMAGE_MIME_TYPES:
        return GenericResponse(success=False, status_code=400,
                               message="Invalid image type. Only JPEG, PNG, and JPG are allowed.")

    file_extension = os.path.splitext(image_file.filename)[1].lower()
    if file_extension not in ALLOWED_IMAGE_EXTENSIONS:
        return GenericResponse(success=False, status_code=400,
                               message="Invalid file extension. Only .jpg, .jpeg, .png are allowed.")

    influencer_service = InfluencerService(db)
    return influencer_service.upload_image(influencer_id=influencer_id, image_file=image_file)


@router.post("/metric/create")
def create_influencer_metric(request: InfluencerMetricRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.create_influencer_metric(request=request)


@router.post("/update/{influencer_id}")
def update_influencer(influencer_id: int, request: UpdateInfluencerRequest,
                      db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.update_influencer(influencer_id=influencer_id, request=request)


@router.post("/metric/update/{influencer_metric_id}")
def update_influencer_metric(influencer_metric_id: int, request: UpdateInfluencerMetricRequest,
                             db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.update_influencer_metric(influencer_metric_id=influencer_metric_id, request=request)


@router.get("/get/{influencer_id}", response_model=None)
def get_influencer_detail(influencer_id: int, db=Depends(db_manager.get_db)) -> Influencer | GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.get_influencer_detail(influencer_id=influencer_id)


@router.get("/metric/get/{influencer_id}", response_model=None)
def get_influencer_metric_detail(influencer_id: int,
                                 db=Depends(db_manager.get_db)) -> InfluencerMetric | GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.get_influencer_metric_detail(influencer_id=influencer_id)


@router.post('/get/insight/{influencer_id}')
def get_influencer_insight(influencer_id: int, db=Depends(db_manager.get_db)) -> InfluencerDetail | GenericResponse:
    user_service = UserService(db)
    return user_service.get_influencer_insight(request=InfluencerInsights(user_id=2, influencer_id=influencer_id))
