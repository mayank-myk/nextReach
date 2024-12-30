from fastapi import APIRouter, Depends, UploadFile, File

from app.database.session import DatabaseSessionManager
from app.requests.influencer_metrics_request import InfluencerMetricRequest
from app.requests.influencer_request import InfluencerRequest
from app.response.generic_response import GenericResponse
from app.services.influencer_service import InfluencerService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/influencer',
    tags=['influencer']
)

db_manager = DatabaseSessionManager()


@router.post("/create")
def create_influencer(request: InfluencerRequest, image_file: UploadFile = File(...),
                      db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.create_influencer(request=request, image_file=image_file)


@router.post("/create/metric")
def create_influencer_metric(request: InfluencerMetricRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.create_influencer_metric(request=request)


@router.post("/update/{influencer_id}")
def update_influencer(influencer_id: int, request: InfluencerRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.update_influencer(influencer_id=influencer_id, request=request)


@router.post("/update/metric/{influencer_metric_id}")
def update_influencer_metric(influencer_metric_id: int, request: InfluencerMetricRequest,
                             db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.update_influencer_metric(influencer_metric_id=influencer_metric_id, request=request)
