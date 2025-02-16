from datetime import datetime

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse

from app.api_requests.client_request import ClientRequest
from app.api_requests.create_collab import CreateCollab
from app.api_requests.update_client_request import UpdateClientRequest
from app.database.client_table import Client
from app.database.session import DatabaseSessionManager
from app.response.generic_response import GenericResponse
from app.services.admin_service import AdminService
from app.services.client_service import ClientService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/client',
    tags=['Client Resources (Only For Admins)']
)

db_manager = DatabaseSessionManager()


@router.get("/get/profile/{phone_number}", response_model=None)
def get_client_profile_from_phone_number(phone_number: str, db=Depends(db_manager.get_db)) -> Client | GenericResponse:
    admin_service = AdminService(db)
    return admin_service.get_client_profile(phone_number=phone_number)


@router.post("/create")
def create_client_profile(request: ClientRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_client(request=request)


@router.post("/update/profile/{client_id}")
def update_client_profile(client_id: int, request: UpdateClientRequest,
                          db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_client(client_id=client_id, request=request)


@router.post("/recharge/{client_id}/{coin_count}")
def recharge_coin(client_id: int, coin_count: int, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.recharge_coin(client_id=client_id, coin_count=coin_count)


@router.post("/create/collab")
def request_collab_on_behalf_of_client(background_tasks: BackgroundTasks, request: CreateCollab,
                                       db=Depends(db_manager.get_db)) -> GenericResponse:
    client_service = ClientService(db)
    return client_service.request_collab(background_tasks=background_tasks, created_by=request.created_by,
                                         client_id=request.client_id,
                                         influencer_id=request.influencer_id, collab_date=None)


@router.post("/signups")
def get_new_logins_report(db=Depends(db_manager.get_db)):
    client_service = ClientService(db)
    excel_file = client_service.get_unique_logins()

    filename = f'Signups_{datetime.today().strftime("%Y-%m-%d")}.xlsx'

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
