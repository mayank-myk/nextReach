from typing import List, Union

from fastapi import APIRouter, Depends
from fastapi.params import Query

from app.api_requests.expense_request import ExpenseRequest
from app.api_requests.revenue_request import RevenueRequest
from app.database.expense_table import Expense
from app.database.revenue_table import Revenue
from app.database.session import DatabaseSessionManager
from app.response.generic_response import GenericResponse
from app.services.admin_service import AdminService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1',
    tags=['Expense, Revenue, Bills (Only For Admins)']
)

db_manager = DatabaseSessionManager()


@router.get("/generate/bill/{campaign_id}")
def generate_bill(campaign_id: int, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.generate_bill(campaign_id=campaign_id)


@router.post("/revenue/create")
def create_revenue(request: RevenueRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_revenue(request=request)


@router.post("/revenue/update/{revenue_id}")
def update_revenue(revenue_id: int, request: RevenueRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_revenue(revenue_id=revenue_id, request=request)


@router.get("/revenue/get/all", response_model=None)
def get_all_revenue(page_number: int = Query(0, description="Page number to fetch", ge=0),
                    page_size: int = Query(100, description="Number of leads per page", ge=1, le=1000),
                    db=Depends(db_manager.get_db)) -> Union[List[Revenue], GenericResponse]:
    admin_service = AdminService(db)
    return admin_service.get_all_revenue(page_size=page_size, page_number=page_number)


@router.post("/expense/create")
def create_expense(request: ExpenseRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.create_expense(request=request)


@router.post("/expense/update/{expense_id}")
def update_expense(expense_id: int, request: ExpenseRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    admin_service = AdminService(db)
    return admin_service.update_expense(expense_id=expense_id, request=request)


@router.get("/expense/get/all", response_model=None)
def get_all_expense(page_number: int = Query(0, description="Page number to fetch", ge=0),
                    page_size: int = Query(100, description="Number of leads per page", ge=1, le=1000),
                    db=Depends(db_manager.get_db)) -> Union[List[Expense], GenericResponse]:
    admin_service = AdminService(db)
    return admin_service.get_all_expense(page_size=page_size, page_number=page_number)
