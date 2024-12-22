from app.repository.client_repository import ClientRepository
from app.repository.expense_repository import ExpenseRepository
from app.repository.revenue_repository import RevenueRepository
from app.requests.admin_user_request import AdminUserRequest
from app.repository.admin_user_repository import AdminUserRepository
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
                return LoginResponse(success=True, error_message=None, admin_type=admin_user.admin_type)
            else:
                return LoginResponse(success=False, error_message="Incorrect password", admin_type=None)
        else:
            return LoginResponse(success=False, error_message="User Id does not exists", admin_type=None)

    def generate_bill(self, campaign_id: str) -> GenericResponse:
        pass

    def create_user(self, new_user: AdminUserRequest) -> GenericResponse:
        new_admin_user = self.admin_user_repository.create_admin(request=new_user)

        if new_admin_user:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None, error_message="Unable to create new admin")

    def update_user(self, user: AdminUserRequest) -> GenericResponse:
        new_admin_user = self.admin_user_repository.update_admin(request=user)

        if new_admin_user:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None, error_message="No admin found for given user_id")

    def delete_user(self, user_id: str) -> GenericResponse:
        admin_user = self.admin_user_repository.delete_admin(user_id=user_id)

        if admin_user:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None, error_message="No admin found for given user_id")

    def create_revenue(self, request: RevenueRequest) -> GenericResponse:
        new_revenue = self.revenue_repository.create_revenue(request=request)

        if new_revenue:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None, error_message="Unable to create new revenue")

    def update_revenue(self, revenue_id: str, request: RevenueRequest) -> GenericResponse:
        new_revenue = self.revenue_repository.update_revenue(revenue_id=revenue_id, request=request)

        if new_revenue:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None,
                                   error_message="No revenue found for given revenue_id")

    def create_expense(self, request: ExpenseRequest) -> GenericResponse:
        new_expense = self.expense_repository.create_expense(request=request)

        if new_expense:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None, error_message="Unable to create new revenue")

    def update_expense(self, expense_id: str, request: ExpenseRequest) -> GenericResponse:
        new_expense = self.expense_repository.update_expense(expense_id=expense_id, request=request)

        if new_expense:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None,
                                   error_message="No expense found for given expense_id")

    def create_client(self, request: ClientRequest) -> GenericResponse:
        timestamp_id = id_utils.get_user_id()
        new_client = self.client_repository.create_client(client_id=timestamp_id, request=request)

        if new_client:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None, error_message="Unable to create new client")

    def update_client(self, client_id: str, request: ClientRequest) -> GenericResponse:
        new_client = self.client_repository.update_client_from_admin(client_id=client_id, request=request)

        if new_client:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None,
                                   error_message="No client found for given client_id")
