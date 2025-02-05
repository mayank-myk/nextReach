from datetime import datetime
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.profile_visit_table import ProfileVisit
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class ProfileVisitRepository:

    def __init__(self, db: Session):
        self.db = db

    def log_profile_visit(self, client_id: int, influencer_id: int) -> ProfileVisit:
        """Creates a new profile visit log for a client viewing an influencer's profile."""
        try:
            profile_visit = ProfileVisit(
                client_id=client_id,
                influencer_id=influencer_id
            )
            self.db.add(profile_visit)
            self.db.commit()
            self.db.refresh(profile_visit)
            return profile_visit
        except SQLAlchemyError as ex:
            self.db.rollback()
            _log.error(f"Error logging profile visit for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))
        except Exception as ex:
            _log.error(
                f"Exception while logging profile visit for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))

    def check_if_influencer_already_visited(self, client_id: int, influencer_id: int) -> int:
        """Counts total visits by a client to a specific influencer."""
        try:
            count = self.db.query(ProfileVisit).filter(
                ProfileVisit.client_id == client_id,
                ProfileVisit.influencer_id == influencer_id
            ).count()
            return count
        except SQLAlchemyError as ex:
            _log.error(f"Error getting total visits for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))
        except Exception as ex:
            _log.error(
                f"Exception while getting total profile visits for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))

    def get_all_influencers_visited(self, client_id: int, influencer_ids: List[int]) -> List[int]:
        try:
            visted_influencer_ids = self.db.query(ProfileVisit.influencer_id).filter(
                ProfileVisit.client_id == client_id, ProfileVisit.influencer_id.in_(influencer_ids)
            ).all()

            return visted_influencer_ids
        except SQLAlchemyError as ex:
            _log.error(f"Error getting all visited influencers for client {client_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))
        except Exception as ex:
            _log.error(
                f"Exception while getting all visited influencers for client {client_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))

    def log_already_visited_profile(self, client_id: int, influencer_id: int) -> ProfileVisit:
        """Creates a new profile visit log for a client viewing an influencer's profile."""
        try:
            exisiting_profile_visit = self.db.query(ProfileVisit).filter(
                ProfileVisit.client_id == client_id, ProfileVisit.influencer_id == influencer_id).order_by(
                ProfileVisit.created_at.desc()).first()

            setattr(exisiting_profile_visit, 'last_visited_at', datetime.now())

            self.db.commit()
            self.db.refresh(exisiting_profile_visit)
            return exisiting_profile_visit
        except SQLAlchemyError as ex:
            self.db.rollback()
            _log.error(
                f"Error updating last_visited_at profile visit for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))
        except Exception as ex:
            _log.error(
                f"Exception updating last_visited_at profile visit for for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))
