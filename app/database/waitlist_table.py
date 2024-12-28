from sqlalchemy import Column, String, DateTime, Enum, Integer
import datetime

from app.database.session import Base
from app.enums.entity_type import EntityType
from app.enums.status import Status


class WaitList(Base):
    __tablename__ = 'waitlist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    entity_type = Column(Enum(EntityType), nullable=False)
    name = Column(String(255), nullable=False)  # Name as a string with a length constraint
    phone_number = Column(String(10), nullable=False)  # Phone number with a length constraint of 10
    email = Column(String(255), nullable=True)
    social_media_handle = Column(String(255), nullable=True)
    onboarding_status = Column(Enum(Status), default=Status.PROCESSING, nullable=False)  # Using Enum for Status
    message = Column(String(1000), nullable=True)
