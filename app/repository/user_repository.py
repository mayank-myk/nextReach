from typing import Optional

from sqlalchemy.orm import Session

from app.database.user_table import User
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.requests.profile_update import ProfileUpdate
from app.requests.user_request import UserRequest
from app.utils.config import get_config
from app.utils.logger import configure_logger

_log = configure_logger()


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user_from_admin(self, user_id: str, request: UserRequest) -> User:
        try:
            new_user = User(
                # id=user_id,
                created_by=request.created_by,
                last_updated_by=request.created_by,
                name=request.name,
                phone_number=request.phone_number,
                business_name=request.business_name,
                email=request.email,
                city=request.city,
                niche=request.niche,
                category=request.category,
                total_profile_visited=0,
                balance_profile_visits=get_config("DEFAULT_PROFILE_VISIT"),
                insta_username=request.insta_username,
                insta_profile_link=request.insta_profile_link,
                insta_followers=request.insta_followers,
                yt_username=request.yt_username,
                yt_profile_link=request.yt_profile_link,
                yt_followers=request.yt_followers,
                fb_username=request.fb_username,
                fb_profile_link=request.fb_profile_link,
                fb_followers=request.fb_followers,
            )

            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except Exception as ex:
            _log.error(f"Unable to create new_user record with user_id {user_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, user_id)

    def update_user_from_admin(self, user_id: str, request: UserRequest) -> Optional[User]:
        try:
            existing_user = self.db.query(User).filter(User.id == user_id).first()

            if not existing_user:
                return None

            if hasattr(request, 'name'):
                setattr(existing_user, 'name', request.name)

            if hasattr(request, 'created_by'):
                setattr(existing_user, 'last_updated_by', request.created_by)

            if hasattr(request, 'business_name'):
                setattr(existing_user, 'business_name', request.business_name)

            if hasattr(request, 'email'):
                setattr(existing_user, 'email', request.email)

            if hasattr(request, 'city'):
                setattr(existing_user, 'city', request.city)

            if hasattr(request, 'niche'):
                setattr(existing_user, 'niche', request.niche)

            if hasattr(request, 'category'):
                setattr(existing_user, 'category', request.category)

            if hasattr(request, 'balance_profile_visits'):
                setattr(existing_user, 'balance_profile_visits', request.balance_profile_visits)

            if hasattr(request, 'insta_username'):
                setattr(existing_user, 'insta_username', request.insta_username)

            if hasattr(request, 'insta_profile_link'):
                setattr(existing_user, 'insta_profile_link', request.insta_profile_link)

            if hasattr(request, 'insta_followers'):
                setattr(existing_user, 'insta_followers', request.insta_followers)

            if hasattr(request, 'yt_username'):
                setattr(existing_user, 'yt_username', request.yt_username)

            if hasattr(request, 'yt_profile_link'):
                setattr(existing_user, 'yt_profile_link', request.yt_profile_link)

            if hasattr(request, 'yt_followers'):
                setattr(existing_user, 'yt_followers', request.yt_followers)

            if hasattr(request, 'fb_username'):
                setattr(existing_user, 'fb_username', request.fb_username)

            if hasattr(request, 'fb_profile_link'):
                setattr(existing_user, 'fb_profile_link', request.fb_profile_link)

            if hasattr(request, 'fb_followers'):
                setattr(existing_user, 'fb_followers', request.fb_followers)

            self.db.commit()
            self.db.refresh(existing_user)
            return existing_user
        except Exception as ex:
            _log.error(f"Unable to update user record with user_id {user_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, user_id)

    def update_user_from_user(self, user_id: str, request: ProfileUpdate) -> Optional[User]:
        try:
            existing_user = self.db.query(User).filter(User.id == user_id).first()

            if not existing_user:
                return None

            setattr(existing_user, 'last_updated_by', user_id)

            if hasattr(request, 'name'):
                setattr(existing_user, 'name', request.name)

            if hasattr(request, 'business_name'):
                setattr(existing_user, 'business_name', request.business_name)

            if hasattr(request, 'email'):
                setattr(existing_user, 'email', request.email)

            if hasattr(request, 'city'):
                setattr(existing_user, 'city', request.city)

            if hasattr(request, 'niche'):
                setattr(existing_user, 'niche', request.niche)

            if hasattr(request, 'category'):
                setattr(existing_user, 'category', request.category)

            if hasattr(request, 'insta_username'):
                setattr(existing_user, 'insta_username', request.insta_username)

            if hasattr(request, 'yt_username'):
                setattr(existing_user, 'yt_username', request.yt_username)

            if hasattr(request, 'fb_username'):
                setattr(existing_user, 'fb_username', request.fb_username)

            self.db.commit()
            self.db.refresh(existing_user)
            return existing_user
        except Exception as ex:
            _log.error(f"Unable to update user record with user_id {user_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, user_id)

    def update_profile_visit_count(self, user_id: str) -> bool:
        try:
            existing_user = self.db.query(User).filter(User.id == user_id).first()

            if not existing_user:
                _log.error("While updating profile visit count, No record found for user with user_id {}".format(
                    user_id))
                return False

            setattr(existing_user, 'total_profile_visited', existing_user.total_profile_visited + 1)
            setattr(existing_user, 'balance_profile_visits', existing_user.balance_profile_visits - 1)

            self.db.commit()
            self.db.refresh(existing_user)
            return True
        except Exception as ex:
            _log.error(f"Unable to update user record with user_id {user_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, user_id)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_or_create_user_by_phone_number(self, phone_number: str) -> Optional[User]:
        user_optional = self.db.query(User).filter(User.phone_number == phone_number).first()
        if user_optional:
            return user_optional
        else:
            new_user = User(
                # id=user_id,
                created_by='system',
                last_updated_by='system',
                phone_number=phone_number
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
