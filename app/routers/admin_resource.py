from fastapi import APIRouter, Depends
from fastapi.params import Query

from app.database.session import DatabaseSessionManager
from app.models.status import Status
from app.requests.admin_user_request import AdminUserRequest
from app.requests.client_request import ClientRequest
from app.requests.expense_request import ExpenseRequest
from app.requests.login_request import LoginRequest
from app.requests.revenue_request import RevenueRequest
from app.response.generic_response import GenericResponse
from app.response.login_response import LoginResponse
from app.services.admin_service import AdminService
from app.services.web_service import WebService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/admin',
    tags=['admin']
)

db_manager = DatabaseSessionManager()


@router.post("/login")
def admin_login(request: LoginRequest, db=Depends(db_manager.get_db)) -> LoginResponse:
    admin_service = AdminService(db)
    return admin_service.admin_login(request=request)


@router.get("/generate/bill/{campaign_id}")
def generate_bill(campaign_id: str, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.generate_bill(campaign_id=campaign_id)


@router.post("/create")
def create_user(user: AdminUserRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_user(new_user=user)


@router.post("/update")
def update_user(user: AdminUserRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_user(user=user)


@router.put("/delete")
def delete_user(user_id: str, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.delete_user(user_id=user_id)


@router.post("/create/revenue")
def create_revenue(request: RevenueRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_revenue(request=request)


@router.post("/update/revenue/{revenue_id}")
def update_revenue(revenue_id: str, request: RevenueRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_revenue(revenue_id=revenue_id, request=request)


@router.get("/get/revenue/all")
def get_all_revenue(page_number: int = Query(0, description="Page number to fetch", ge=0),
                    page_size: int = Query(100, description="Number of leads per page", ge=1, le=1000),
                    db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.get_all_expense(page_size=page_size, page_number=page_number)


@router.post("/create/expense")
def create_expense(request: ExpenseRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_expense(request=request)


@router.post("/update/expense/{expense_id}")
def update_expense(expense_id: str, request: ExpenseRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_expense(expense_id=expense_id, request=request)


@router.get("/get/expense/all")
def get_all_expense(page_number: int = Query(0, description="Page number to fetch", ge=0),
                    page_size: int = Query(100, description="Number of leads per page", ge=1, le=1000),
                    db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.get_all_expense(page_size=page_size, page_number=page_number)


@router.post("/create/client")
def create_client(request: ClientRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_client(request=request)


@router.post("/update/client/{client_id}")
def update_client(client_id: str, request: ClientRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_client(client_id=client_id, request=request)


@router.post("/update/lead/status/{wait_list_id}")
def create_lead(wait_list_id: str, status: Status, db=Depends(db_manager.get_db)) -> GenericResponse:
    web_service = WebService(db)
    return web_service.update_lead(wait_list_id=wait_list_id, status=status)


@router.get("/get/lead/all")
def get_all_leads(page_number: int = Query(0, description="Page number to fetch", ge=0),
                  page_size: int = Query(100, description="Number of leads per page", ge=1, le=1000),
                  db=Depends(db_manager.get_db)) -> GenericResponse:
    web_service = WebService(db)
    return web_service.get_all_leads(page_size=page_size, page_number=page_number)
