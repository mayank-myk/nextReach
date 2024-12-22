from sqlalchemy.orm import Session

from app.database.watchlist_table import WatchList
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class WatchListRepository:

    def __init__(self, db: Session):
        self.db = db

    def add_to_watchlist(self, user_id: str, influencer_id: str) -> WatchList:
        try:
            new_collab = WatchList(
                user_id=user_id,
                influencer_id=influencer_id
            )

            self.db.add(new_collab)
            self.db.commit()
            self.db.refresh(new_collab)
            return new_collab
        except Exception as ex:
            _log.error("Unable to add watchlist request for user_id {}".format(user_id))
            raise FetchOneUserMetadataException(ex, user_id)
