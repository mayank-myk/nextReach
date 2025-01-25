from typing import Optional, List

from sqlalchemy.orm import Session

from app.api_requests.blog_request import BlogRequest
from app.database.blog_table import Blog
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class BlogRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_blog(self, request: BlogRequest) -> Blog:
        try:
            new_blog = Blog(
                created_at=request.created_at,
                author=request.author,
                url=request.url,
                title=request.title,
                category=request.category,
                blog_image=request.blog_image
            )

            self.db.add(new_blog)
            self.db.commit()
            self.db.refresh(new_blog)
            return new_blog
        except Exception as ex:
            _log.error(f"Unable to create blog. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, request.title)

    def update_blog(self, blog_id: int, request: BlogRequest) -> Optional[Blog]:
        try:
            existing_blog = self.db.query(Blog).filter(Blog.id == blog_id).first()

            if not existing_blog:
                return None

            if hasattr(request, 'created_at') and request.created_at is not None:
                setattr(existing_blog, 'created_at', request.created_at)

            if hasattr(request, 'author') and request.author is not None:
                setattr(existing_blog, 'author', request.author)

            if hasattr(request, 'url') and request.url is not None:
                setattr(existing_blog, 'url', request.url)

            if hasattr(request, 'title') and request.title is not None:
                setattr(existing_blog, 'title', request.title)

            if hasattr(request, 'category') and request.category is not None:
                setattr(existing_blog, 'category', request.category)

            if hasattr(request, 'blog_image') and request.blog_image is not None:
                setattr(existing_blog, 'blog_image', request.blog_image)

            self.db.commit()
            self.db.refresh(existing_blog)
            return existing_blog
        except Exception as ex:
            _log.error(f"Unable to update Blog with blog_id {blog_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, blog_id)

    def get_blog_by_blog_url(self, url: str) -> Optional[Blog]:

        try:
            existing_blog = self.db.query(Blog).filter(Blog.url == url).first()
            if not existing_blog:
                return None
            return existing_blog

        except Exception as ex:
            _log.error(f"Unable to fetch blog record with blog_id {url}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, url)

    def get_all_blogs(self) -> Optional[List[Blog]]:

        try:
            return self.db.query(Blog).limit(6).offset(0).all()

        except Exception as ex:
            _log.error(f"Unable to fetch all blog records. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, "Blog")
