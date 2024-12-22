from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
import datetime
from sqlalchemy.orm import relationship
from app.database.session import Base


class ProfileVisit(Base):
    __tablename__ = 'profile_visit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    influencer_id = Column(String(13), ForeignKey('influencer.id'), nullable=False)
    client_id = Column(String(13), ForeignKey('client.id'), nullable=False)
    influencer = relationship("Influencer", back_populates="profile_visit")
    client = relationship("Client", back_populates="profile_visit")
