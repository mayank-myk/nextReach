import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base


class ProfileVisit(Base):
    __tablename__ = 'profile_visit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_visited_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    influencer_id = Column(Integer, ForeignKey('influencer.id'), nullable=False, index=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False, index=True)
    influencer = relationship("Influencer", back_populates="profile_visit")
    client = relationship("Client", back_populates="profile_visit")
