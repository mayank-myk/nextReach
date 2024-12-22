from typing import Optional, List

from sqlalchemy.orm import Session

from app.database.revenue_table import Revenue
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.requests.revenue_request import RevenueRequest
from app.utils.logger import configure_logger

_log = configure_logger()


class RevenueRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_revenue(self, request: RevenueRequest) -> Revenue:
        try:
            new_revenue = Revenue(
                created_by=request.created_by,
                last_updated_by=request.created_by,
                type=request.type,
                date=request.date,
                amount=request.amount,
                description=request.description,
                mode_of_payment=request.mode_of_payment,
                account_id=request.account_id,
                campaign_id=request.campaign_id,
                paid_by=request.paid_by,
            )

            self.db.add(new_revenue)
            self.db.commit()
            self.db.refresh(new_revenue)
            return new_revenue
        except Exception as ex:
            _log.error(f"Unable to create revenue for campaign_id {request.campaign_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(request.campaign_id))

    def update_revenue(self, revenue_id: int, request: RevenueRequest) -> Optional[Revenue]:
        try:
            existing_revenue = self.db.get(Revenue, revenue_id)

            if not existing_revenue:
                return None

            setattr(existing_revenue, 'last_updated_by', request.created_by)
            setattr(existing_revenue, 'type', request.type)
            setattr(existing_revenue, 'date', request.date)
            setattr(existing_revenue, 'amount', request.amount)
            setattr(existing_revenue, 'description', request.description)
            setattr(existing_revenue, 'mode_of_payment', request.mode_of_payment)
            setattr(existing_revenue, 'account_id', request.account_id)
            setattr(existing_revenue, 'paid_by', request.paid_by)

            self.db.commit()
            self.db.refresh(existing_revenue)
            return existing_revenue
        except Exception as ex:
            _log.error(f"Unable to update revenue for revenue_id {revenue_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(revenue_id))

    def get_revenue_by_id(self, revenue_id: int) -> Optional[Revenue]:

        try:
            existing_revenue = self.db.get(Revenue, revenue_id)

            if not existing_revenue:
                return None

            return existing_revenue

        except Exception as ex:
            _log.error(f"Unable to fetch revenue for revenue_id {revenue_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(revenue_id))

    def get_all_revenue(self, limit: int, offset: int) -> Optional[List[Revenue]]:
        try:
            return self.db.query(Revenue).offset(offset).limit(limit).all()
        except Exception as ex:
            raise FetchOneUserMetadataException(ex, str(offset))
