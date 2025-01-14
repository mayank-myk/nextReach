from typing import List

from fastapi import APIRouter, Depends
from fastapi.params import Query

from app.database.session import DatabaseSessionManager
from app.database.waitlist_table import WaitList
from app.enums.status import Status
from app.response.generic_response import GenericResponse
from app.services.admin_service import AdminService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/lead',
    tags=['Create/Update Leads (Only For Admins)']
)

db_manager = DatabaseSessionManager()


@router.post("/update/status/{wait_list_id}")
def create_lead(wait_list_id: int, status: Status, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_lead(wait_list_id=wait_list_id, status=status)


@router.get("/get/all", response_model=None)
def get_all_leads(page_number: int = Query(0, description="Page number to fetch", ge=0),
                  page_size: int = Query(100, description="Number of leads per page", ge=1, le=1000),
                  db=Depends(db_manager.get_db)) -> List[WaitList] | GenericResponse:
    admin_service = AdminService(db)
    return admin_service.get_all_leads(page_size=page_size, page_number=page_number)
