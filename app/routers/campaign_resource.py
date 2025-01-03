from app.database.session import DatabaseSessionManager
from app.api_requests.campaign_request import CampaignRequest
from app.response.generic_response import GenericResponse
from app.services.campaign_service import CampaignService
from app.utils.logger import configure_logger
from fastapi import APIRouter, Depends

_log = configure_logger()

router = APIRouter(
    prefix='/v1/campaign',
    tags=['campaign']
)

db_manager = DatabaseSessionManager()


@router.post("/create")
def create_campaign(request: CampaignRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.create_campaign(request=request)


@router.post("/update/{campaign_id}")
def update_campaign(campaign_id: int, request: CampaignRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign(campaign_id=campaign_id, request=request)
