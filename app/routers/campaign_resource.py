from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api_requests.campaign_completion_request import CampaignCompletionRequest
from app.api_requests.campaign_content_post_request import CampaignContentPostRequest
from app.api_requests.campaign_day2_billing_request import CampaignDay2BillingRequest
from app.api_requests.campaign_day8_billing_request import CampaignDay8BillingRequest
from app.api_requests.campaign_draft_approved_request import CampaignDraftApprovedRequest
from app.api_requests.campaign_influencer_finalized_request import CampaignInfluencerFinalizedRequest
from app.api_requests.campaign_pending_deliverables_request import CampaignPendingDeliverables
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


@router.post("/move-to/influencer-finalized/{campaign_id}")
def move_campaign_to_influencer_finalized_stage(campaign_id: int, request: CampaignInfluencerFinalizedRequest,
                                                db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign_to_influencer_finalization(campaign_id=campaign_id, request=request)


@router.post("/move-to/shoot-completed/{campaign_id}")
def move_campaign_to_shoot_completed_stage(campaign_id: int, content_shoot_date: date,
                                           db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign_to_shoot_completed(campaign_id=campaign_id,
                                                               content_shoot_date=content_shoot_date)


@router.post("/move-to/draft-approved/{campaign_id}")
def move_campaign_to_draft_approved_stage(campaign_id: int, request: CampaignDraftApprovedRequest,
                                          db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign_to_draft_approved(campaign_id=campaign_id, request=request)


@router.post("/move-to/content-posted/{campaign_id}")
def move_campaign_to_content_posted_stage(campaign_id: int, request: CampaignContentPostRequest,
                                          db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign_to_content_posted(campaign_id=campaign_id, request=request)


@router.post("/move-to/day2-billing/{campaign_id}")
def move_campaign_to_day2_billing_stage(campaign_id: int, request: CampaignDay2BillingRequest,
                                        db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign_to_day2_billing(campaign_id=campaign_id, request=request)


@router.post("/move-to/day8-billing/{campaign_id}")
def move_campaign_to_day8_billing_stage(campaign_id: int, request: CampaignDay8BillingRequest,
                                        db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign_to_day8_billing(campaign_id=campaign_id, request=request)


@router.post("/move-to/completed/{campaign_id}")
def move_campaign_to_completed_stage(campaign_id: int, request: Optional[CampaignCompletionRequest] = None,
                                     db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign_to_completed(campaign_id=campaign_id, request=request)


@router.post("/move-to/cancelled/{campaign_id}")
def move_campaign_to_cancelled_stage(campaign_id: int, db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign_to_cancelled(campaign_id=campaign_id)


@router.post("/update/pending-deliverables/{campaign_id}")
def update_campaign_pending_deliverables(campaign_id: int, request: CampaignPendingDeliverables,
                                         db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign_pending_deliverables(campaign_id=campaign_id, request=request)


@router.post("/create")
def create_campaign(request: CampaignRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.create_campaign(request=request)


@router.post("/update/{campaign_id}")
def update_campaign(campaign_id: int, request: UpdateCampaignRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.update_campaign(campaign_id=campaign_id, request=request)


@router.get("/get/detail/{campaign_id}")
def get_campaign_detail(campaign_id: int, db=Depends(db_manager.get_db)) -> CampaignDetail | GenericResponse:
    campaign_service = CampaignService(db)
    return campaign_service.get_client_campaign_detail(campaign_id=campaign_id)


@router.get("/get/dump")
def get_all_active_campaign_detail(db=Depends(db_manager.get_db)):
    campaign_service = CampaignService(db)
    excel_file = campaign_service.get_all_active_campaign_detail()

    filename = f'Campaigns_{datetime.today().strftime("%Y-%m-%d")}.xlsx'

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
