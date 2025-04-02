import datetime

from sqlalchemy import Column, String, DateTime, Integer, Enum, ARRAY, CheckConstraint, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.enums.campaign_stage import CampaignStage
from app.enums.content_type import ContentType
from app.enums.payment_status import PaymentStatus


class Campaign(Base):
    __tablename__ = "campaign"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                             nullable=False)
    created_by = Column(String(255), nullable=False)  # Assuming min_length=5 is being enforced
    last_updated_by = Column(String(255), nullable=False)  # Assuming min_length=5 is being enforced
    campaign_managed_by = Column(String(255), nullable=False)  # Assuming min_length=5 is being enforced

    # Foreign Keys
    influencer_id = Column(Integer, ForeignKey('influencer.id'), nullable=False, index=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False, index=True)

    # Campaign stage and content info
    stage = Column(Enum(CampaignStage), nullable=False)
    content_charge = Column(Integer, CheckConstraint('content_charge >= 0'), nullable=True)
    views_charge = Column(Integer, CheckConstraint('views_charge >= 0'), nullable=True)
    fixed_charge = Column(Integer, CheckConstraint('fixed_charge >= 0'), nullable=True)
    type_of_content = Column(Enum(ContentType), nullable=True)
    campaign_notes = Column(String(1000), nullable=True)

    # Ratings and reviews
    rating = Column(Integer, CheckConstraint('rating >= 0 AND rating <= 5'),
                    nullable=True)  # Assuming rating is from 0 to 5
    review = Column(String(1000), nullable=True)  # Review can be large text

    # Influencer finalization information
    influencer_finalization_date = Column(Date, nullable=True)

    # Content creation information
    content_shoot_date = Column(Date, nullable=True)

    # Content draft approved information
    content_draft_date = Column(Date, nullable=True)
    content_billing_amount = Column(Integer, CheckConstraint('content_billing_amount >= 0'), nullable=True)
    content_billing_payment_at = Column(DateTime, nullable=True)
    content_billing_payment_status = Column(Enum(PaymentStatus), nullable=True)

    # Content post information
    content_post_date = Column(DateTime, nullable=True)
    insta_post_link = Column(String(255), nullable=True)
    yt_post_link = Column(String(255), nullable=True)
    fb_post_link = Column(String(255), nullable=True)

    # First billing
    first_billing_date = Column(Date, nullable=True)
    first_billing_views = Column(Integer, CheckConstraint('first_billing_views >= 0'), nullable=True)
    first_billing_likes = Column(Integer, CheckConstraint('first_billing_likes >= 0'), nullable=True)
    first_billing_comments = Column(Integer, CheckConstraint('first_billing_comments >= 0'), nullable=True)
    first_billing_shares = Column(Integer, CheckConstraint('first_billing_shares >= 0'), nullable=True)
    first_billing_amount = Column(Integer, CheckConstraint('first_billing_amount >= 0'), nullable=True)
    first_billing_payment_at = Column(DateTime, nullable=True)
    first_billing_payment_status = Column(Enum(PaymentStatus), nullable=True)

    # Second billing
    second_billing_date = Column(Date, nullable=True)
    second_billing_views = Column(Integer, CheckConstraint('second_billing_views >= 0'), nullable=True)
    second_billing_likes = Column(Integer, CheckConstraint('second_billing_likes >= 0'), nullable=True)
    second_billing_comments = Column(Integer, CheckConstraint('second_billing_comments >= 0'), nullable=True)
    second_billing_shares = Column(Integer, CheckConstraint('second_billing_shares >= 0'), nullable=True)
    second_billing_amount = Column(Integer, CheckConstraint('second_billing_amount >= 0'), nullable=True)
    second_billing_payment_at = Column(DateTime, nullable=True)
    second_billing_payment_status = Column(Enum(PaymentStatus), nullable=True)

    post_insights = Column(ARRAY(String), nullable=True)
    pending_deliverables = Column(ARRAY(String), nullable=True)

    influencer = relationship("Influencer", back_populates="campaign")
    client = relationship("Client", back_populates="campaign")
    revenue = relationship("Revenue", back_populates="campaign")
