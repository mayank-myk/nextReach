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
            _log.error("Unable to create revenue for campaign_id {}".format(request.campaign_id))
            raise FetchOneUserMetadataException(ex, request.campaign_id)

    def update_revenue(self, revenue_id: str, request: RevenueRequest) -> Revenue:
        try:
            existing_revenue = await self.db.get(Revenue, revenue_id)

            if not existing_revenue:
                _log.info("No record found for revenue with with revenue_id {}".format(revenue_id))
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
            _log.error("Unable to update revenue for revenue_id {}".format(revenue_id))
            raise FetchOneUserMetadataException(ex, revenue_id)

    def get_revenue_by_id(self, revenue_id: str) -> Revenue:

        try:
            existing_revenue = await self.db.get(Revenue, revenue_id)

            if not existing_revenue:
                _log.info("No record found for revenue with with revenue_id {}".format(revenue_id))
                return None

            return existing_revenue

        except Exception as ex:
            _log.error("Unable to fetch revenue for revenue_id {}".format(revenue_id))
            raise FetchOneUserMetadataException(ex, revenue_id)
