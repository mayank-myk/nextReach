from typing import Optional, List

from sqlalchemy.orm import Session

from app.api_requests.next_reach_academy_request import NextReachAcademyRequest
from app.database.academy_video_table import AcademyVideo
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class AcademyVideoRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_nra(self, request: NextReachAcademyRequest) -> AcademyVideo:
        try:
            ss = AcademyVideo(
                yt_link=request.yt_link,
                title=request.title,
                category=request.category,
                tag1=request.tag1,
                tag2=request.tag2,
                tag3=request.tag3,
                tag4=request.tag4
            )

            self.db.add(ss)
            self.db.commit()
            self.db.refresh(ss)
            return ss
        except Exception as ex:
            _log.error(f"Unable to create NextReachAcademy. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, request.title)

    def update_nra(self, nra_id: int, request: NextReachAcademyRequest) -> Optional[AcademyVideo]:
        try:
            existing_nra = self.db.query(AcademyVideo).filter(AcademyVideo.id == nra_id).first()

            if not existing_nra:
                return None

            if hasattr(request, 'tag1') and request.tag1 is not None:
                setattr(existing_nra, 'tag1', request.tag1)

            if hasattr(request, 'tag2') and request.tag2 is not None:
                setattr(existing_nra, 'tag2', request.tag2)

            if hasattr(request, 'tag3') and request.tag3 is not None:
                setattr(existing_nra, 'tag3', request.tag3)

            if hasattr(request, 'tag4') and request.tag4 is not None:
                setattr(existing_nra, 'tag4', request.tag4)

            if hasattr(request, 'category') and request.category is not None:
                setattr(existing_nra, 'category', request.category)

            if hasattr(request, 'yt_link') and request.yt_link is not None:
                setattr(existing_nra, 'yt_link', request.yt_link)

            if hasattr(request, 'title') and request.title is not None:
                setattr(existing_nra, 'title', request.title)

            self.db.commit()
            self.db.refresh(existing_nra)
            return existing_nra
        except Exception as ex:
            _log.error(f"Unable to update NextReachAcademy with nra_id {nra_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, nra_id)

    def get_all_nra(self) -> Optional[List[AcademyVideo]]:

        try:
            return self.db.query(AcademyVideo).limit(6).offset(0).all()

        except Exception as ex:
            _log.error(f"Unable to fetch all NextReachAcademy records. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, "NextReachAcademy")
