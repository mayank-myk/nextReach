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
    user_id = Column(Integer, ForeignKey('user_table.id'), nullable=False, index=True)
    influencer = relationship("Influencer", back_populates="profile_visit")
    user = relationship("User", back_populates="profile_visit")
