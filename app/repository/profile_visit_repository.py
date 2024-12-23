from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database.profile_visit_table import ProfileVisit
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class ProfileVisitRepository:

    def __init__(self, db: Session):
        self.db = db

    def log_profile_visit(self, client_id: str, influencer_id: str) -> ProfileVisit:
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
            raise FetchOneUserMetadataException("Error logging profile visit")
        except Exception as ex:
            _log.error(
                f"Exception while logging profile visit for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, client_id)

    def check_if_influencer_already_visited(self, client_id: str, influencer_id: str) -> int:
        """Counts total visits by a client to a specific influencer."""
        try:
            count = self.db.query(ProfileVisit).filter(
                ProfileVisit.client_id == client_id,
                ProfileVisit.influencer_id == influencer_id
            ).count()
            return count
        except SQLAlchemyError as ex:
            _log.error(f"Error getting total visits for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException("Error getting total visits")
        except Exception as ex:
            _log.error(
                f"Exception while getting total profile visits for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, client_id)

    def get_total_visits_by_client(self, client_id: str) -> int:
        """Counts total visits by a client to a specific influencer."""
        try:
            count = self.db.query(ProfileVisit).filter(
                ProfileVisit.client_id == client_id
            ).count()
            return count
        except SQLAlchemyError as ex:
            _log.error(f"Error getting total visits for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException("Error getting total visits")
        except Exception as ex:
            _log.error(
                f"Exception while getting total profile visits for client {client_id} to influencer {influencer_id}: {str(ex)}")
            raise FetchOneUserMetadataException(ex, client_id)