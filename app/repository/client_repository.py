from typing import Optional

from sqlalchemy.orm import Session

from app.database.client_table import Client
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.requests.client_request import ClientRequest
from app.requests.profile_update import ProfileUpdate
from app.utils.config import get_config
from app.utils.logger import configure_logger

_log = configure_logger()


class ClientRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_client(self, client_id: str, request: ClientRequest) -> Client:
        try:
            new_client = Client(
                id=client_id,
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

            self.db.add(new_client)
            self.db.commit()
            self.db.refresh(new_client)
            return new_client
        except Exception as ex:
            _log.error("Unable to create new_client record with client_id {}".format(client_id))
            raise FetchOneUserMetadataException(ex, client_id)

    def update_client_from_admin(self, client_id: str, request: ClientRequest) -> Optional[Client]:
        try:
            existing_client = self.db.query(Client).filter(Client.id == client_id).first()

            if not existing_client:
                return None

            if hasattr(request, 'name'):
                setattr(existing_client, 'name', request.name)

            if hasattr(request, 'created_by'):
                setattr(existing_client, 'last_updated_by', request.created_by)

            if hasattr(request, 'business_name'):
                setattr(existing_client, 'business_name', request.business_name)

            if hasattr(request, 'email'):
                setattr(existing_client, 'email', request.email)

            if hasattr(request, 'city'):
                setattr(existing_client, 'city', request.city)

            if hasattr(request, 'niche'):
                setattr(existing_client, 'niche', request.niche)

            if hasattr(request, 'category'):
                setattr(existing_client, 'category', request.category)

            if hasattr(request, 'balance_profile_visits'):
                setattr(existing_client, 'balance_profile_visits', request.balance_profile_visits)

            if hasattr(request, 'insta_username'):
                setattr(existing_client, 'insta_username', request.insta_username)

            if hasattr(request, 'insta_profile_link'):
                setattr(existing_client, 'insta_profile_link', request.insta_profile_link)

            if hasattr(request, 'insta_followers'):
                setattr(existing_client, 'insta_followers', request.insta_followers)

            if hasattr(request, 'yt_username'):
                setattr(existing_client, 'yt_username', request.yt_username)

            if hasattr(request, 'yt_profile_link'):
                setattr(existing_client, 'yt_profile_link', request.yt_profile_link)

            if hasattr(request, 'yt_followers'):
                setattr(existing_client, 'yt_followers', request.yt_followers)

            if hasattr(request, 'fb_username'):
                setattr(existing_client, 'fb_username', request.fb_username)

            if hasattr(request, 'fb_profile_link'):
                setattr(existing_client, 'fb_profile_link', request.fb_profile_link)

            if hasattr(request, 'fb_followers'):
                setattr(existing_client, 'fb_followers', request.fb_followers)

            self.db.commit()
            self.db.refresh(existing_client)
            return existing_client
        except Exception as ex:
            _log.error("Unable to update client record with client_id {}".format(client_id))
            raise FetchOneUserMetadataException(ex, client_id)

    def update_client_from_user(self, client_id: str, request: ProfileUpdate) -> Optional[Client]:
        try:
            existing_client = self.db.query(Client).filter(Client.id == client_id).first()

            if not existing_client:
                return None

            setattr(existing_client, 'last_updated_by', client_id)

            if hasattr(request, 'name'):
                setattr(existing_client, 'name', request.name)

            if hasattr(request, 'business_name'):
                setattr(existing_client, 'business_name', request.business_name)

            if hasattr(request, 'email'):
                setattr(existing_client, 'email', request.email)

            if hasattr(request, 'city'):
                setattr(existing_client, 'city', request.city)

            if hasattr(request, 'niche'):
                setattr(existing_client, 'niche', request.niche)

            if hasattr(request, 'category'):
                setattr(existing_client, 'category', request.category)

            if hasattr(request, 'insta_username'):
                setattr(existing_client, 'insta_username', request.insta_username)

            if hasattr(request, 'yt_username'):
                setattr(existing_client, 'yt_username', request.yt_username)

            if hasattr(request, 'fb_username'):
                setattr(existing_client, 'fb_username', request.fb_username)

            self.db.commit()
            self.db.refresh(existing_client)
            return existing_client
        except Exception as ex:
            _log.error("Unable to update client record with client_id {}".format(client_id))
            raise FetchOneUserMetadataException(ex, client_id)

    def update_profile_visit_count(self, client_id: str) -> bool:
        try:
            existing_client = self.db.query(Client).filter(Client.id == client_id).first()

            if not existing_client:
                _log.error("While updating profile visit count, No record found for client with client_id {}".format(
                    client_id))
                return False

            setattr(existing_client, 'total_profile_visited', existing_client.total_profile_visited + 1)
            setattr(existing_client, 'balance_profile_visits', existing_client.balance_profile_visits - 1)

            self.db.commit()
            self.db.refresh(existing_client)
            return True
        except Exception as ex:
            _log.error("Unable to update client record with client_id {}".format(client_id))
            raise FetchOneUserMetadataException(ex, client_id)

    def get_client_by_id(self, client_id: str) -> Optional[Client]:
        return self.db.query(Client).filter(Client.id == client_id).first()

    def get_client_by_phone_number(self, phone_number: str) -> Optional[Client]:
        return self.db.query(Client).filter(Client.phone_number == phone_number).first()
