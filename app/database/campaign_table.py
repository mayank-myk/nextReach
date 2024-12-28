import datetime

from sqlalchemy import Column, String, DateTime, Integer, Enum, ARRAY, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.enums.campaign_stage import CampaignStage
from app.enums.content_type import ContentType
from app.enums.status import Status


class Campaign(Base):
    __tablename__ = "campaign"

    # Primary Key
    id = Column(String(13), primary_key=True, unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                             nullable=False)
    created_by = Column(String(255), nullable=False)  # Assuming min_length=5 is being enforced
    last_updated_by = Column(String(255), nullable=False)  # Assuming min_length=5 is being enforced
    campaign_managed_by = Column(String(255), nullable=False)  # Assuming min_length=5 is being enforced

    # Foreign Keys
    influencer_id = Column(String(13), ForeignKey('influencer.id'), nullable=False)
    client_id = Column(String(13), ForeignKey('client.id'), nullable=False)

    # Campaign stage and content info
    stage = Column(Enum(CampaignStage), nullable=False)
    content_charge = Column(Integer, CheckConstraint('content_charge >= 0'), nullable=True)
    views_charge = Column(Integer, CheckConstraint('views_charge >= 0'), nullable=True)
    type_of_content = Column(Enum(ContentType), nullable=True)
    campaign_notes = Column(String(255), nullable=True)

    # Ratings and reviews
    rating = Column(Integer, CheckConstraint('rating >= 0 AND rating <= 5'),
                    nullable=True)  # Assuming rating is from 0 to 5
    review = Column(String(1000), nullable=True)  # Review can be large text

    # Influencer finalization information
    influencer_finalization_date = Column(DateTime, nullable=True)

    # Content creation information
    content_shoot_date = Column(DateTime, nullable=True)

    # Content post information
    insta_post_link = Column(String(255), nullable=True)
    youtube_post_link = Column(String(255), nullable=True)
    fb_post_link = Column(String(255), nullable=True)
    content_post_date = Column(DateTime, nullable=True)
    content_billing_amount = Column(Integer, CheckConstraint('content_billing_amount >= 0'), nullable=True)
    content_billing_payment_at = Column(DateTime, nullable=True)
    content_billing_payment_status = Column(Enum(Status), nullable=True)

    # First billing
    first_billing_date = Column(DateTime, nullable=True)
    first_billing_views = Column(Integer, CheckConstraint('first_billing_views >= 0'), nullable=True)
    first_billing_likes = Column(Integer, CheckConstraint('first_billing_likes >= 0'), nullable=True)
    first_billing_comments = Column(Integer, CheckConstraint('first_billing_comments >= 0'), nullable=True)
    first_billing_shares = Column(Integer, CheckConstraint('first_billing_shares >= 0'), nullable=True)
    first_billing_amount = Column(Integer, CheckConstraint('first_billing_amount >= 0'), nullable=True)
    first_billing_payment_at = Column(DateTime, nullable=True)
    first_billing_payment_status = Column(Enum(Status), nullable=True)

    # Second billing
    second_billing_date = Column(DateTime, nullable=True)
    second_billing_views = Column(Integer, CheckConstraint('second_billing_views >= 0'), nullable=True)
    second_billing_likes = Column(Integer, CheckConstraint('second_billing_likes >= 0'), nullable=True)
    second_billing_comments = Column(Integer, CheckConstraint('second_billing_comments >= 0'), nullable=True)
    second_billing_shares = Column(Integer, CheckConstraint('second_billing_shares >= 0'), nullable=True)
    second_billing_amount = Column(Integer, CheckConstraint('second_billing_amount >= 0'), nullable=True)
    second_billing_payment_at = Column(DateTime, nullable=True)
    second_billing_payment_status = Column(Enum(Status), nullable=True)

    # Third billing
    third_billing_date = Column(DateTime, nullable=True)
    third_billing_views = Column(Integer, CheckConstraint('third_billing_views >= 0'), nullable=True)
    third_billing_likes = Column(Integer, CheckConstraint('third_billing_likes >= 0'), nullable=True)
    third_billing_comments = Column(Integer, CheckConstraint('third_billing_comments >= 0'), nullable=True)
    third_billing_shares = Column(Integer, CheckConstraint('third_billing_shares >= 0'), nullable=True)
    third_billing_amount = Column(Integer, CheckConstraint('third_billing_amount >= 0'), nullable=True)
    third_billing_payment_at = Column(DateTime, nullable=True)
    third_billing_payment_status = Column(Enum(Status), nullable=True)

    post_insights = Column(ARRAY(String), nullable=True)
    pending_deliverables = Column(ARRAY(String), nullable=True)

    influencer = relationship("Influencer", back_populates="profile_visit")
    client = relationship("Client", back_populates="profile_visit")
