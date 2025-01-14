from typing import Optional

from sqlalchemy.orm import Session

from app.api_requests.client_request import ClientRequest
from app.api_requests.profile_update import ProfileUpdate
from app.api_requests.update_client_request import UpdateClientRequest
from app.database.client_table import Client
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class ClientRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_client_from_admin(self, request: ClientRequest) -> Client:
        try:
            new_client = Client(
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
                balance_profile_visits=20,
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
            _log.error(f"Unable to create new_client record with phone_number {request.phone_number}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, request.phone_number)

    def update_client_from_admin(self, client_id: int, request: UpdateClientRequest) -> Optional[Client]:
        try:
            existing_client = self.db.query(Client).filter(Client.id == client_id).first()

            if not existing_client:
                return None

            if hasattr(request, 'name') and request.name is not None:
                setattr(existing_client, 'name', request.name)

            if hasattr(request, 'updated_by') and request.updated_by is not None:
                setattr(existing_client, 'last_updated_by', request.updated_by)

            if hasattr(request, 'business_name') and request.business_name is not None:
                setattr(existing_client, 'business_name', request.business_name)

            if hasattr(request, 'email') and request.email is not None:
                setattr(existing_client, 'email', request.email)

            if hasattr(request, 'city') and request.city is not None:
                setattr(existing_client, 'city', request.city)

            if hasattr(request, 'niche') and request.niche is not None:
                setattr(existing_client, 'niche', request.niche)

            if hasattr(request, 'category') and request.category is not None:
                setattr(existing_client, 'category', request.category)

            if hasattr(request, 'insta_username') and request.insta_username is not None:
                setattr(existing_client, 'insta_username', request.insta_username)

            if hasattr(request, 'insta_profile_link') and request.insta_profile_link is not None:
                setattr(existing_client, 'insta_profile_link', request.insta_profile_link)

            if hasattr(request, 'insta_followers') and request.insta_followers is not None:
                setattr(existing_client, 'insta_followers', request.insta_followers)

            if hasattr(request, 'yt_username') and request.yt_username is not None:
                setattr(existing_client, 'yt_username', request.yt_username)

            if hasattr(request, 'yt_profile_link') and request.yt_profile_link is not None:
                setattr(existing_client, 'yt_profile_link', request.yt_profile_link)

            if hasattr(request, 'yt_followers') and request.yt_followers is not None:
                setattr(existing_client, 'yt_followers', request.yt_followers)

            if hasattr(request, 'fb_username') and request.fb_username is not None:
                setattr(existing_client, 'fb_username', request.fb_username)

            if hasattr(request, 'fb_profile_link') and request.fb_profile_link is not None:
                setattr(existing_client, 'fb_profile_link', request.fb_profile_link)

            if hasattr(request, 'fb_followers') and request.fb_followers is not None:
                setattr(existing_client, 'fb_followers', request.fb_followers)

            self.db.commit()
            self.db.refresh(existing_client)
            return existing_client
        except Exception as ex:
            _log.error(f"Unable to update client record with client_id {client_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))

    def coin_recharge(self, client_id: int, coin_count: int) -> Optional[Client]:
        try:
            existing_client = self.db.query(Client).filter(Client.id == client_id).first()

            if not existing_client:
                return None

            setattr(existing_client, 'balance_profile_visits', coin_count)

            self.db.commit()
            self.db.refresh(existing_client)
            return existing_client
        except Exception as ex:
            _log.error(f"Unable to recharge client with client_id {client_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))

    def update_client_from_client(self, client_id: int, request: ProfileUpdate) -> Optional[Client]:
        try:
            existing_client = self.db.query(Client).filter(Client.id == client_id).first()

            if not existing_client:
                return None

            setattr(existing_client, 'last_updated_by', "client_" + str(client_id))

            if hasattr(request, 'name') and request.name is not None:
                setattr(existing_client, 'name', request.name)

            if hasattr(request, 'business_name') and request.business_name is not None:
                setattr(existing_client, 'business_name', request.business_name)

            if hasattr(request, 'email') and request.email is not None:
                setattr(existing_client, 'email', request.email)

            if hasattr(request, 'city') and request.city is not None:
                setattr(existing_client, 'city', request.city)

            if hasattr(request, 'niche') and request.niche is not None:
                setattr(existing_client, 'niche', request.niche)

            if hasattr(request, 'category') and request.category is not None:
                setattr(existing_client, 'category', request.category)

            if hasattr(request, 'insta_username') and request.insta_username is not None:
                setattr(existing_client, 'insta_username', request.insta_username)

            if hasattr(request, 'yt_username') and request.yt_username is not None:
                setattr(existing_client, 'yt_username', request.yt_username)

            if hasattr(request, 'fb_username') and request.fb_username is not None:
                setattr(existing_client, 'fb_username', request.fb_username)

            self.db.commit()
            self.db.refresh(existing_client)
            return existing_client
        except Exception as ex:
            _log.error(f"Unable to update client record with client_id {client_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))

    def update_profile_visit_count(self, client_id: int) -> bool:
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
            _log.error(f"Unable to update client record with client_id {client_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(client_id))

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        return self.db.query(Client).filter(Client.id == client_id).first()

    def get_client_by_phone_number(self, phone_number: str) -> Optional[Client]:
        return self.db.query(Client).filter(Client.phone_number == phone_number).first()

    def get_or_create_client_by_phone_number(self, phone_number: str) -> Optional[Client]:
        client_optional = self.db.query(Client).filter(Client.phone_number == phone_number).first()
        if client_optional:
            return client_optional
        else:
            new_client = Client(
                created_by='system',
                last_updated_by='system',
                phone_number=phone_number
            )
            self.db.add(new_client)
            self.db.commit()
            self.db.refresh(new_client)
            return new_client
