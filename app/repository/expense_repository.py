from typing import Optional, List

from sqlalchemy.orm import Session

from app.database.expense_table import Expense
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.requests.expense_request import ExpenseRequest
from app.utils.logger import configure_logger

_log = configure_logger()


class ExpenseRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_expense(self, request: ExpenseRequest) -> Expense:
        try:
            new_revenue = Expense(
                created_by=request.created_by,
                last_updated_by=request.created_by,
                type=request.type,
                date=request.date,
                amount=request.amount,
                description=request.description,
                mode_of_payment=request.mode_of_payment,
                account_id=request.account_id
            )

            self.db.add(new_revenue)
            self.db.commit()
            self.db.refresh(new_revenue)
            return new_revenue
        except Exception as ex:
            _log.error("Unable to create expense for account_id: {}".format(request.account_id))
            raise FetchOneUserMetadataException(ex, request.account_id)

    def update_expense(self, expense_id: str, request: ExpenseRequest) -> Optional[Expense]:
        try:
            existing_expense = self.db.get(Expense, expense_id)

            if not existing_expense:
                return None

            setattr(existing_expense, 'last_updated_by', request.created_by)
            setattr(existing_expense, 'type', request.type)
            setattr(existing_expense, 'date', request.date)
            setattr(existing_expense, 'amount', request.amount)
            setattr(existing_expense, 'description', request.description)
            setattr(existing_expense, 'mode_of_payment', request.mode_of_payment)
            setattr(existing_expense, 'account_id', request.account_id)

            self.db.commit()
            self.db.refresh(existing_expense)
            return existing_expense
        except Exception as ex:
            _log.error("Unable to update expense for expense_id {}".format(expense_id))
            raise FetchOneUserMetadataException(ex, expense_id)

    def get_all_expense(self, limit: int, offset: int) -> Optional[List[Expense]]:
        try:
            return self.db.query(Expense).offset(offset).limit(limit).all()

        except Exception as ex:
            raise FetchOneUserMetadataException(ex, str(offset))

    def get_expense_by_id(self, expense_id: str) -> Optional[Expense]:
        try:
            existing_expense = self.db.get(Expense, expense_id)

            if not existing_expense:
                return None

            return existing_expense

        except Exception as ex:
            _log.error("Unable to update expense for expense_id {}".format(expense_id))
            raise FetchOneUserMetadataException(ex, expense_id)
