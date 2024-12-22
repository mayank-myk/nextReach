from typing import List

from app.database.expense_table import Expense
from app.database.revenue_table import Revenue
from app.repository.admin_user_repository import AdminUserRepository
from app.repository.client_repository import ClientRepository
from app.repository.expense_repository import ExpenseRepository
from app.repository.revenue_repository import RevenueRepository
from app.requests.admin_user_request import AdminUserRequest
from app.requests.client_request import ClientRequest
from app.requests.expense_request import ExpenseRequest
from app.requests.login_request import LoginRequest
from app.requests.revenue_request import RevenueRequest
from app.response.generic_response import GenericResponse
from app.response.login_response import LoginResponse
from app.utils import id_utils
from app.utils.logger import configure_logger

_log = configure_logger()


class AdminService:
    def __init__(self, session):
        self.admin_user_repository = AdminUserRepository(session)
        self.revenue_repository = RevenueRepository(session)
        self.expense_repository = ExpenseRepository(session)
        self.client_repository = ClientRepository(session)

    def admin_login(self, request: LoginRequest) -> LoginResponse:
        admin_user = self.admin_user_repository.get_admin_by_user_id(user_id=request.user_id)
        if admin_user:
            if admin_user.password == request.password:
                return LoginResponse(success=True, message=None, admin_type=admin_user.admin_type)
            else:
                return LoginResponse(success=False, message="Incorrect password", admin_type=None)
        else:
            _log.info("No record found for admin login with user_id {}".format(request.user_id))
            return LoginResponse(success=False, message="User Id does not exists", admin_type=None)

    def generate_bill(self, campaign_id: str) -> GenericResponse:
        pass

    def create_user(self, new_user: AdminUserRequest) -> GenericResponse:
        new_admin_user = self.admin_user_repository.create_admin(request=new_user)

        if new_admin_user:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            return GenericResponse(success=False, button_text=None, message="Unable to create new admin")

    def update_user(self, user: AdminUserRequest) -> GenericResponse:
        new_admin_user = self.admin_user_repository.update_admin(request=user)

        if new_admin_user:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("No record found for admin with user_id {}".format(user.user_id))
            return GenericResponse(success=False, button_text=None, message="No admin found for given user_id")

    def delete_user(self, user_id: str) -> GenericResponse:
        admin_user = self.admin_user_repository.delete_admin(user_id=user_id)

        if admin_user:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("No record found for admin with user_id {}".format(user_id))
            return GenericResponse(success=False, button_text=None, message="No admin found for given user_id")

    def create_revenue(self, request: RevenueRequest) -> GenericResponse:
        new_revenue = self.revenue_repository.create_revenue(request=request)

        if new_revenue:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            return GenericResponse(success=False, button_text=None, message="Unable to create new revenue")

    def update_revenue(self, revenue_id: str, request: RevenueRequest) -> GenericResponse:
        new_revenue = self.revenue_repository.update_revenue(revenue_id=revenue_id, request=request)

        if new_revenue:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("No record found for revenue with with revenue_id {}".format(revenue_id))
            return GenericResponse(success=False, button_text=None,
                                   message="No revenue found for given revenue_id")

    def get_all_revenue(self, page_size: int, page_number: int) -> List[Revenue] | GenericResponse:
        expenses = self.revenue_repository.get_all_revenue(limit=page_size, offset=page_size * page_number)

        if expenses and len(expenses) > 0:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("No record found for revenue page_size {}, page_number {}".format(page_size, page_number))
            return GenericResponse(success=False, button_text=None,
                                   message="No record found for revenue at all")

    def create_expense(self, request: ExpenseRequest) -> GenericResponse:
        new_expense = self.expense_repository.create_expense(request=request)

        if new_expense:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            return GenericResponse(success=False, button_text=None, message="Unable to create new revenue")

    def update_expense(self, expense_id: str, request: ExpenseRequest) -> GenericResponse:
        new_expense = self.expense_repository.update_expense(expense_id=expense_id, request=request)

        if new_expense:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("No record found for expense with expense_id {}".format(expense_id))
            return GenericResponse(success=False, button_text=None,
                                   message="No expense found for given expense_id")

    def get_all_expense(self, page_size: int, page_number: int) -> List[Expense] | GenericResponse:
        expenses = self.expense_repository.get_all_expense(limit=page_size, offset=page_size * page_number)

        if expenses and len(expenses) > 0:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("No record found for expense page_size {}, page_number {}".format(page_size, page_number))
            return GenericResponse(success=False, button_text=None,
                                   message="No record found for expense at all")

    def create_client(self, request: ClientRequest) -> GenericResponse:
        timestamp_id = id_utils.get_user_id()
        new_client = self.client_repository.create_client(client_id=timestamp_id, request=request)

        if new_client:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("Unable to create new client with client_id {}".format(timestamp_id))
            return GenericResponse(success=False, button_text=None, message="Unable to create new client")

    def update_client(self, client_id: str, request: ClientRequest) -> GenericResponse:
        new_client = self.client_repository.update_client_from_admin(client_id=client_id, request=request)

        if new_client:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("No record found for client with client_id {}".format(client_id))
            return GenericResponse(success=False, button_text=None,
                                   message="No client found for given client_id")
