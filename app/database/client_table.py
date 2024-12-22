import datetime

from sqlalchemy import Column, String, DateTime, Integer, Enum, CheckConstraint
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.enums.business_category import BusinessCategory
from app.enums.city import City
from app.enums.niche import Niche


class Client(Base):
    __tablename__ = "client"

    # Primary Key
    id = Column(String(13), primary_key=True, unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                             nullable=False)
    created_by = Column(String(255), nullable=False)
    last_updated_by = Column(String(255), nullable=False)

    # Client information
    name = Column(String(255), nullable=False)
    phone_number = Column(String(10), nullable=False)  # Phone is unique and fixed length
    business_name = Column(String(255), nullable=True)  # Business name should be present
    email = Column(String(255), nullable=True)  # Email can be checked using validation logic
    city = Column(Enum(City), nullable=True)  # Enum for predefined cities
    niche = Column(Enum(Niche), nullable=True)  # Enum for predefined niches
    category = Column(Enum(BusinessCategory), nullable=True)  # Enum for predefined business categories

    # Profile tracking
    total_profile_visited = Column(Integer, CheckConstraint('total_profile_visited >= 0'), default=0, nullable=False)
    balance_profile_visits = Column(Integer, CheckConstraint('balance_profile_visits >= 0'), default=20, nullable=False)

    # Social media handles
    insta_username = Column(String(255), nullable=True)  # Assuming min_length=3
    insta_profile_link = Column(String(255), nullable=True)  # URL link to profile
    insta_followers = Column(Integer, CheckConstraint('insta_followers >= 0'), default=0,
                             nullable=True)  # No negative followers

    yt_username = Column(String(255), nullable=True)  # Assuming min_length=3
    yt_profile_link = Column(String(255), nullable=True)  # URL link to YouTube profile
    yt_followers = Column(Integer, CheckConstraint('yt_followers >= 0'), default=0,
                          nullable=True)  # No negative followers

    fb_username = Column(String(255), nullable=True)  # Assuming min_length=3
    fb_profile_link = Column(String(255), nullable=True)  # URL link to Facebook profile
    fb_followers = Column(Integer, CheckConstraint('fb_followers >= 0'), default=0,
                          nullable=True)  # No negative followers

    # The relationship
    profile_visit = relationship(
        "ProfileVisit",
        back_populates="client",
        cascade="all, delete-orphan"
    )
    collab = relationship(
        "Collab",
        back_populates="client",
        cascade="all, delete-orphan"
    )
