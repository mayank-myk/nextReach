from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api_requests.campaign_request import CampaignRequest
from app.api_requests.update_campaign_request import UpdateCampaignRequest
from app.database.session import DatabaseSessionManager
from app.response.campaign_detail import CampaignDetail
from app.response.generic_response import GenericResponse
from app.services.campaign_service import CampaignService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/campaign',
    tags=['Campaign Resources (Only For Admins)']
)

db_manager = DatabaseSessionManager()


@router.post("/create")
def create_campaign(request: CampaignRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.create_campaign(request=request)


@router.post("/update/{campaign_id}")
def update_campaign(campaign_id: int, request: UpdateCampaignRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign(campaign_id=campaign_id, request=request)


@router.get("/detail/{campaign_id}")
def get_client_campaign_detail(campaign_id: int, db=Depends(db_manager.get_db)) -> CampaignDetail | GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.get_client_campaign_detail(campaign_id=campaign_id)


@router.get("/get/dump")
def get_all_active_campaign_detail(db=Depends(db_manager.get_db)):
    campaign_service = CampaignService(db)
    excel_file = campaign_service.get_all_active_campaign_detail()

    filename = f'Campaigns{datetime.today().strftime("%Y-%m-%d")}.xlsx'

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
