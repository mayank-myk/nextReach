from sqlalchemy.orm import Session

from app.database.client_table import Client
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.requests.client_request import ClientRequest
from app.requests.profile_update import ProfileUpdate
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
            _log.error("Unable to create new_client record with phone_number {}".format(request.phone_number))
            raise FetchOneUserMetadataException(ex, request.user_id)

    def update_client_from_admin(self, client_id: str, request: ClientRequest) -> Client:
        try:
            existing_client = self.db.query(Client).filter(Client.id == client_id).first()

            if not existing_client:
                _log.info("No record found for client with client_id {}".format(client_id))
                return None

            existing_client = Client(
                id=existing_client.id,
                name=request.name,
                created_by=existing_client.created_by,
                last_updated_by=request.created_by,
                phone_number=existing_client.phone_number,
                business_name=request.business_name,
                email=request.email,
                city=request.city,
                niche=request.niche,
                category=request.category,
                total_profile_visited=existing_client.total_profile_visited,
                balance_profile_visits=request.balance_profile_visits,
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

            self.db.commit()
            self.db.refresh(existing_client)
            return existing_client
        except Exception as ex:
            _log.error("Unable to update client record with client_id {}".format(client_id))
            raise FetchOneUserMetadataException(ex, request.user_id)

    def update_client_from_user(self, client_id: str, request: ProfileUpdate) -> Client:
        try:
            existing_client = self.db.query(Client).filter(Client.id == client_id).first()

            if not existing_client:
                _log.info("No record found for client with client_id {}".format(client_id))
                return None

            existing_client = Client(
                id=existing_client.id,
                name=request.name,
                created_by=existing_client.created_by,
                last_updated_by=client_id,
                phone_number=existing_client.phone_number,
                business_name=request.business_name,
                email=request.email,
                city=request.city,
                niche=request.niche,
                category=request.category,
                total_profile_visited=existing_client.total_profile_visited,
                balance_profile_visits=existing_client.total_profile_visited,
                insta_username=request.insta_username,
                insta_profile_link=existing_client.insta_profile_link,
                insta_followers=existing_client.insta_followers,
                yt_username=request.yt_username,
                yt_profile_link=existing_client.yt_profile_link,
                yt_followers=existing_client.yt_followers,
                fb_username=request.fb_username,
                fb_profile_link=existing_client.fb_profile_link,
                fb_followers=existing_client.fb_followers,
            )

            self.db.commit()
            self.db.refresh(existing_client)
            return existing_client
        except Exception as ex:
            _log.error("Unable to update client record with client_id {}".format(client_id))
            raise FetchOneUserMetadataException(ex, request.user_id)

    def update_profile_visit_count(self, client_id: str) -> Client:
        try:
            existing_client = self.db.query(Client).filter(Client.id == client_id).first()

            if not existing_client:
                _log.info("No record found for client with client_id {}".format(client_id))
                return None

            existing_client = Client(
                id=existing_client.id,
                name=request.name,
                created_by=existing_client.created_by,
                last_updated_by=client_id,
                phone_number=existing_client.phone_number,
                business_name=request.business_name,
                email=request.email,
                city=request.city,
                niche=request.niche,
                category=request.category,
                total_profile_visited=existing_client.total_profile_visited,
                balance_profile_visits=existing_client.total_profile_visited,
                insta_username=request.insta_username,
                insta_profile_link=existing_client.insta_profile_link,
                insta_followers=existing_client.insta_followers,
                yt_username=request.yt_username,
                yt_profile_link=existing_client.yt_profile_link,
                yt_followers=existing_client.yt_followers,
                fb_username=request.fb_username,
                fb_profile_link=existing_client.fb_profile_link,
                fb_followers=existing_client.fb_followers,
            )

            self.db.commit()
            self.db.refresh(existing_client)
            return existing_client
        except Exception as ex:
            _log.error("Unable to update client record with client_id {}".format(client_id))
            raise FetchOneUserMetadataException(ex, request.user_id)

    def get_client_by_id(self, client_id: str) -> Client:
        return self.db.query(Client).filter(Client.id == client_id).first()
