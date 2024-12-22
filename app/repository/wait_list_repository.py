from typing import List, Optional

from sqlalchemy.orm import Session

from app.database.waitlist_table import WaitList
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.models.status import Status
from app.requests.waitlist_request import WaitListRequest
from app.utils.logger import configure_logger

_log = configure_logger()


class WaitListRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_wait_list(self, request: WaitListRequest) -> WaitList:
        try:

            db_wait_list = WaitList(
                entity_type=request.entity_type,
                name=request.name,
                phone_number=request.phone_number,
                email=request.email,
                social_media_handle=request.social_media_handle,
                onboarding_status=request.onboarding_status,
                message=request.message
            )

            self.db.add(db_wait_list)
            self.db.commit()
            self.db.refresh(db_wait_list)
            return db_wait_list
        except Exception as ex:
            _log.error("Unable to create wait_list record for phone_number {}".format(request.phone_number))
            raise FetchOneUserMetadataException(ex, request.phone_number)

    def update_wait_list_status(self, wait_list_id: str, status: Status) -> Optional[WaitList]:
        try:
            db_wait_list = self.db.query(WaitList).filter(WaitList.id == wait_list_id).first()

            if not db_wait_list:
                return None

            setattr(db_wait_list, 'onboarding_status', status)

            self.db.commit()
            self.db.refresh(db_wait_list)
            return db_wait_list
        except Exception as ex:
            _log.error("Unable to update wait_list record for wait_list_id {}".format(wait_list_id))
            raise FetchOneUserMetadataException(ex, wait_list_id)

    def get_wait_list(self, limit: int, offset: int) -> Optional[List[WaitList]]:
        try:
            return self.db.query(WaitList).offset(offset).limit(limit).all()

        except Exception as ex:
            _log.error("Unable to get wait_list record for page_number {}".format(offset))
            raise FetchOneUserMetadataException(ex, str(offset))
