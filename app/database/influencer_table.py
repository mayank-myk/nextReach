import datetime

from sqlalchemy import Column, String, DateTime, Integer, Enum, ARRAY, CheckConstraint, Date, Boolean
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.content_subject import ContentSubject
from app.enums.content_type import ContentType
from app.enums.gender import Gender
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform


class Influencer(Base):
    __tablename__ = "influencer"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                             nullable=False)
    created_by = Column(String(255), nullable=False)
    last_updated_by = Column(String(255), nullable=False)

    # Influencer information
    primary_platform = Column(Enum(Platform), nullable=False)
    name = Column(String(255), nullable=False)  # Assuming min_length=5 is being enforced
    gender = Column(Enum(Gender), nullable=True)
    phone_number = Column(String(10), nullable=False)  # Assuming it's a 10-digit phone number
    email = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    upi_id = Column(String(255), nullable=True)
    profile_picture = Column(String(255), nullable=False)  # URL for profile picture
    languages = Column(ARRAY(Enum(Language, name="language_enum")), nullable=True)  # List of languages
    next_reach_score = Column(Integer, CheckConstraint('next_reach_score >= 0'), default=0)
    dob = Column(Date, nullable=True)
    blue_tick = Column(Boolean, nullable=True, default=False)

    # Niche and business location
    niche = Column(ARRAY(Enum(Niche, name="niche_enum")), nullable=True)
    content_type = Column(Enum(ContentType), nullable=True)
    content_subject = Column(Enum(ContentSubject), nullable=True)
    city = Column(Enum(City), nullable=False)
    collab_type = Column(Enum(CollabType), nullable=False)
    deliverables = Column(ARRAY(String), nullable=True)
    content_charge = Column(Integer, CheckConstraint('content_charge >= 0'), default=0)
    views_charge = Column(Integer, CheckConstraint('views_charge >= 0'), default=0)
    fixed_charge = Column(Integer, CheckConstraint('fixed_charge >= 0'), default=0)

    # The relationship to SocialMediaDetail (One-to-Many)
    influencer_insta_metric = relationship(
        "InfluencerInstaMetric",
        back_populates="influencer"
    )
    influencer_yt_metric = relationship(
        "InfluencerYtMetric",
        back_populates="influencer"
    )
    influencer_fb_metric = relationship(
        "InfluencerFbMetric",
        back_populates="influencer"
    )
    campaign = relationship(
        "Campaign",
        back_populates="influencer"
    )
    profile_visit = relationship(
        "ProfileVisit",
        back_populates="influencer"
    )
