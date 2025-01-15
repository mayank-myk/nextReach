from typing import List

from app.api_requests.admin_user_request import AdminUserRequest
from app.api_requests.blog_request import BlogRequest
from app.api_requests.client_request import ClientRequest
from app.api_requests.expense_request import ExpenseRequest
from app.api_requests.login_request import LoginRequest
from app.api_requests.next_reach_academy_request import NextReachAcademyRequest
from app.api_requests.revenue_request import RevenueRequest
from app.api_requests.success_story_request import SuccessStoryRequest
from app.api_requests.update_client_request import UpdateClientRequest
from app.database.client_table import Client
from app.database.expense_table import Expense
from app.database.revenue_table import Revenue
from app.database.waitlist_table import WaitList
from app.enums.status import Status
from app.repository.academy_video_repository import AcademyVideoRepository
from app.repository.admin_user_repository import AdminUserRepository
from app.repository.blog_repository import BlogRepository
from app.repository.campaign_repository import CampaignRepository
from app.repository.client_repository import ClientRepository
from app.repository.expense_repository import ExpenseRepository
from app.repository.influencer_repository import InfluencerRepository
from app.repository.revenue_repository import RevenueRepository
from app.repository.success_story_repository import SuccessStoryRepository
from app.repository.wait_list_repository import WaitListRepository
from app.response.generic_response import GenericResponse
from app.response.login_response import LoginResponse
from app.utils.logger import configure_logger

_log = configure_logger()


class AdminService:
    def __init__(self, session):
        self.admin_user_repository = AdminUserRepository(session)
        self.revenue_repository = RevenueRepository(session)
        self.expense_repository = ExpenseRepository(session)
        self.client_repository = ClientRepository(session)
        self.wait_list_repository = WaitListRepository(session)
        self.campaign_repository = CampaignRepository(session)
        self.influencer_repository = InfluencerRepository(session)
        self.blog_repository = BlogRepository(session)
        self.success_story_repository = SuccessStoryRepository(session)
        self.academy_video_repository = AcademyVideoRepository(session)

    def admin_login(self, request: LoginRequest) -> LoginResponse:
        admin_user = self.admin_user_repository.get_admin_by_admin_id(admin_id=request.admin_id)
        if admin_user:
            if admin_user.password == request.password:
                return LoginResponse(success=True, message=None, admin_type=admin_user.admin_type)
            else:
                return LoginResponse(success=False, message="Incorrect password", admin_type=None)
        else:
            _log.info("No record found for admin login with admin_id {}".format(request.admin_id))
            return LoginResponse(success=False, message="Admin id does not exists", admin_type=None)

    def generate_bill(self, campaign_id: int) -> GenericResponse:
        return GenericResponse(success=False)

    def create_admin(self, new_user: AdminUserRequest) -> GenericResponse:
        new_admin_user = self.admin_user_repository.create_admin(request=new_user)

        if new_admin_user:
            return GenericResponse(success=True, header="Success", message="Successfully created new admin")
        else:
            return GenericResponse(success=False, message="Unable to create new admin")

    def update_admin(self, user: AdminUserRequest) -> GenericResponse:
        new_admin_user = self.admin_user_repository.update_admin(request=user)

        if new_admin_user:
            return GenericResponse(success=True, header="Success", message="Update successful")
        else:
            _log.info("No record found for admin with admin_id {}".format(user.admin_id))
            return GenericResponse(success=False, message="No admin found for given admin_id")

    def delete_admin(self, admin_id: str) -> GenericResponse:
        admin_user = self.admin_user_repository.delete_admin(admin_id=admin_id)

        if admin_user:
            return GenericResponse(success=True, header="Success", message="Successfully deleted the admin")
        else:
            _log.info("No record found for admin with admin_id {}".format(admin_id))
            return GenericResponse(success=False, message="No admin found for given admin_id")

    def create_revenue(self, request: RevenueRequest) -> GenericResponse:
        new_revenue = self.revenue_repository.create_revenue(request=request)

        if new_revenue:
            return GenericResponse(success=True, header="Success",
                                   message=f"Successfully created new revenue with revenue_id: {new_revenue.id}")
        else:
            return GenericResponse(success=False, message="Unable to create new revenue")

    def update_revenue(self, revenue_id: int, request: RevenueRequest) -> GenericResponse:
        new_revenue = self.revenue_repository.update_revenue(revenue_id=revenue_id, request=request)

        if new_revenue:
            return GenericResponse(success=True, header="Success", message="Successfully updated revenue")
        else:
            _log.info("No record found for revenue with revenue_id {}".format(revenue_id))
            return GenericResponse(success=False,
                                   message="No revenue found for given revenue_id")

    def get_all_revenue(self, page_size: int, page_number: int) -> List[Revenue] | GenericResponse:
        revenues = self.revenue_repository.get_all_revenue(limit=page_size, offset=page_size * page_number)

        if revenues and len(revenues) > 0:
            return revenues
        else:
            _log.info("No record found for revenue page_size {}, page_number {}".format(page_size, page_number))
            return GenericResponse(success=False,
                                   message="No record found for revenue at all")

    def create_expense(self, request: ExpenseRequest) -> GenericResponse:
        new_expense = self.expense_repository.create_expense(request=request)

        if new_expense:
            return GenericResponse(success=True, header="Success",
                                   message=f"Successfully created new expense with expense_id: {new_expense.id}")
        else:
            return GenericResponse(success=False, message="Unable to create new expense")

    def update_expense(self, expense_id: int, request: ExpenseRequest) -> GenericResponse:
        new_expense = self.expense_repository.update_expense(expense_id=expense_id, request=request)

        if new_expense:
            return GenericResponse(success=True, header="Success", message="Successfully updated expense")
        else:
            _log.info("No record found for expense with expense_id {}".format(expense_id))
            return GenericResponse(success=False,
                                   message="No expense found for given expense_id")

    def get_all_expense(self, page_size: int, page_number: int) -> List[Expense] | GenericResponse:
        expenses = self.expense_repository.get_all_expense(limit=page_size, offset=page_size * page_number)

        if expenses and len(expenses) > 0:
            return expenses
        else:
            _log.info("No record found for expense page_size {}, page_number {}".format(page_size, page_number))
            return GenericResponse(success=False,
                                   message="No record found for expense at all")

    def get_client_profile(self, phone_number: str) -> Client | GenericResponse:
        existing_client = self.client_repository.get_client_by_phone_number(phone_number=phone_number)
        if not existing_client:
            return GenericResponse(success=False,
                                   message=f"Business client with phone_number: {phone_number} doesn't exists")
        return existing_client

    def create_client(self, request: ClientRequest) -> GenericResponse:
        existing_client = self.client_repository.get_client_by_phone_number(phone_number=request.phone_number)
        if existing_client:
            return GenericResponse(success=True, header="Success",
                                   message=f"Business client with phone_number: {request.phone_number} already exists")
        new_client = self.client_repository.create_client_from_admin(request=request)

        if new_client:
            return GenericResponse(success=True, header="Success",
                                   message=f"Successfully created new business client with client_id: {new_client.id}")
        else:
            _log.info("Unable to create new business client with phone_number {}".format(request.phone_number))
            return GenericResponse(success=False, message="Unable to create new client")

    def update_client(self, client_id: int, request: UpdateClientRequest) -> GenericResponse:
        new_client = self.client_repository.update_client_from_admin(client_id=client_id, request=request)

        if new_client:
            return GenericResponse(success=True, header="Success",
                                   message=f"Successfully updated business client with client_id: {client_id}")
        else:
            _log.info("No record found for client with client_id {}".format(client_id))
            return GenericResponse(success=False,
                                   message=f"No client found for client_id: {client_id}")

    def recharge_coin(self, client_id: int, coin_count: int) -> GenericResponse:
        new_client = self.client_repository.coin_recharge(client_id=client_id, coin_count=coin_count)

        if new_client:
            return GenericResponse(success=True, header="Success",
                                   message=f"Successfully recharged business client with client_id: {client_id}, coin_count: {coin_count}")
        else:
            _log.info("No record found for client with client_id {}".format(client_id))
            return GenericResponse(success=False,
                                   message="No client found for given client_id")

    def update_lead(self, wait_list_id: int, status: Status) -> GenericResponse:
        wait_list = self.wait_list_repository.update_wait_list_status(wait_list_id=wait_list_id, status=status)

        if wait_list:
            return GenericResponse(success=True, header="Success",
                                   message=f"Successfully updated lead status for wait_list_id: {wait_list_id}")
        else:
            _log.info("No record found for wait_list with wait_list_id {}".format(wait_list_id))
            return GenericResponse(success=False,
                                   message="No wait_list found for given wait_list_id")

    def get_all_leads(self, page_size: int, page_number: int) -> List[WaitList] | GenericResponse:
        wait_list = self.wait_list_repository.get_wait_list(limit=page_size, offset=page_size * page_number)

        if wait_list and len(wait_list) > 0:
            return wait_list
        else:
            _log.info("No record found for wait_list page_size {}, page_number {}".format(page_size, page_number))
            return GenericResponse(success=False,
                                   message="No wait_list found for at all")

    def create_blog(self, request: BlogRequest) -> GenericResponse:
        new_blog = self.blog_repository.create_blog(request=request)

        if new_blog:
            return GenericResponse(success=True, header="Success",
                                   message=f"Successfully created new Blog with blog_id: {new_blog.id}")
        else:
            return GenericResponse(success=False, message="Unable to create new blog")

    def update_blog(self, blog_id: int, request: BlogRequest) -> GenericResponse:
        new_blog = self.blog_repository.update_blog(blog_id=blog_id, request=request)

        if new_blog:
            return GenericResponse(success=True, header="Success", message="Successfully updated Blog")
        else:
            _log.info("No record found for blog with blog_id {}".format(blog_id))
            return GenericResponse(success=False,
                                   message="No Blog found for given blog_id")

    def create_ss(self, request: SuccessStoryRequest) -> GenericResponse:
        new_ss = self.success_story_repository.create_ss(request=request)

        if new_ss:
            return GenericResponse(success=True, header="Success",
                                   message=f"Successfully created new success-story with id: {new_ss.id}")
        else:
            return GenericResponse(success=False, message="Unable to create new success-story")

    def update_ss(self, ss_id: int, request: SuccessStoryRequest) -> GenericResponse:
        new_ss = self.success_story_repository.update_ss(ss_id=ss_id, request=request)

        if new_ss:
            return GenericResponse(success=True, header="Success", message="Successfully updated success-story")
        else:
            _log.info("No record found for success-story with ss_id {}".format(ss_id))
            return GenericResponse(success=False,
                                   message="No success-story found for given ss_id")

    def create_nra(self, request: NextReachAcademyRequest) -> GenericResponse:
        new_nra = self.academy_video_repository.create_nra(request=request)

        if new_nra:
            return GenericResponse(success=True, header="Success",
                                   message=f"Successfully created new academy-video with id: {new_nra.id}")
        else:
            return GenericResponse(success=False, message="Unable to create new academy-video")

    def update_nra(self, nra_id: int, request: NextReachAcademyRequest) -> GenericResponse:
        new_nra = self.academy_video_repository.update_nra(nra_id=nra_id, request=request)

        if new_nra:
            return GenericResponse(success=True, header="Success", message="Successfully updated academy-video")
        else:
            _log.info("No record found for academy-video with nra_id {}".format(nra_id))
            return GenericResponse(success=False,
                                   message="No academy-video found for given nra_id")
