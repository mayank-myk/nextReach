from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.database.session import DatabaseSessionManager
from app.enums.status import Status
from app.response.generic_response import GenericResponse
from app.services.admin_service import AdminService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/lead',
    tags=['Leads (Only For Admins)']
)

db_manager = DatabaseSessionManager()


@router.post("/update/status/{wait_list_id}")
def create_lead(wait_list_id: int, status: Status, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_lead(wait_list_id=wait_list_id, status=status)


@router.get("/get/dump")
def get_all_leads_dump(
        db=Depends(db_manager.get_db)):
    admin_service = AdminService(db)
    excel_file = admin_service.get_all_active_leads()

    filename = f'Leads{datetime.today().strftime("%Y-%m-%d")}.xlsx'

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
