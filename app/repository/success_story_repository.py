from typing import Optional, List

from sqlalchemy.orm import Session

from app.api_requests.success_story_request import SuccessStoryRequest
from app.database.success_story_table import SuccessStory
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class SuccessStoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_ss(self, request: SuccessStoryRequest) -> SuccessStory:
        try:
            ss = SuccessStory(
                title=request.title,
                group_name=request.group_name,
                url=request.url,
                tag1=request.tag1,
                tag2=request.tag2,
                business_image=request.business_image,
                influencer_image=request.influencer_image,
                content=request.content
            )

            self.db.add(ss)
            self.db.commit()
            self.db.refresh(ss)
            return ss
        except Exception as ex:
            _log.error(f"Unable to create SuccessStory. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, request.title)

    def update_ss(self, ss_id: int, request: SuccessStoryRequest) -> Optional[SuccessStory]:
        try:
            existing_ss = self.db.query(SuccessStory).filter(SuccessStory.id == ss_id).first()

            if not existing_ss:
                return None

            if hasattr(request, 'tag1') and request.tag1 is not None:
                setattr(existing_ss, 'tag1', request.tag1)

            if hasattr(request, 'tag2') and request.tag2 is not None:
                setattr(existing_ss, 'tag2', request.tag2)

            if hasattr(request, 'url') and request.url is not None:
                setattr(existing_ss, 'url', request.url)

            if hasattr(request, 'title') and request.title is not None:
                setattr(existing_ss, 'title', request.title)

            if hasattr(request, 'group_name') and request.group_name is not None:
                setattr(existing_ss, 'group_name', request.group_name)

            if hasattr(request, 'business_image') and request.business_image is not None:
                setattr(existing_ss, 'business_image', request.business_image)

            if hasattr(request, 'influencer_image') and request.influencer_image is not None:
                setattr(existing_ss, 'influencer_image', request.influencer_image)

            if hasattr(request, 'content') and request.content is not None:
                setattr(existing_ss, 'content', request.content)

            self.db.commit()
            self.db.refresh(existing_ss)
            return existing_ss
        except Exception as ex:
            _log.error(f"Unable to update SuccessStory with ss_id {ss_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, ss_id)

    def get_ss_by_ss_url(self, url: str) -> Optional[SuccessStory]:

        try:
            existing_ss = self.db.query(SuccessStory).filter(SuccessStory.url == url).first()
            if not existing_ss:
                return None
            return existing_ss

        except Exception as ex:
            _log.error(f"Unable to fetch SuccessStory with ss_id {url}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, url)

    def get_all_ss(self) -> Optional[List[SuccessStory]]:

        try:
            return self.db.query(SuccessStory).all()

        except Exception as ex:
            _log.error(f"Unable to fetch all SuccessStory records. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, "SuccessStory")
