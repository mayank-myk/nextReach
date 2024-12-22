import datetime
from sqlalchemy import Column, String, DateTime, Integer, Enum, CheckConstraint, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.client_type import ClientType
from app.models.revenue_type import RevenueType


class Revenue(Base):
    __tablename__ = "revenue"

    # Primary Key (auto-generated id)
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_by = Column(String(255), nullable=False)  # min_length=5
    last_updated_by = Column(String(255), nullable=False)  # min_length=5
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                             nullable=False)

    # Revenue details
    type = Column(Enum(RevenueType), nullable=False)  # Enum type for Revenue
    date = Column(Date, default=datetime.date.today, nullable=False)
    amount = Column(Integer, CheckConstraint('amount >= 1'), nullable=False)  # Amount must be >= 1
    description = Column(String(255), nullable=False)  # Description of the revenue source
    mode_of_payment = Column(String(255), nullable=False)  # Payment method
    account_id = Column(String(255), nullable=False)  # The account used for payment (can be related to another table)
    campaign_id = Column(String(13), ForeignKey('campaign.id'), nullable=False)  # Foreign key to Campaign
    paid_by = Column(Enum(ClientType), nullable=False)  # Paid by, as an enum from ClientType

    # Relationship to Campaign
    revenue = relationship("Campaign", back_populates="revenue")
