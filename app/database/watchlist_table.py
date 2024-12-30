from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
import datetime
from sqlalchemy.orm import relationship
from app.database.session import Base


class WatchList(Base):
    __tablename__ = 'watchlist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    influencer_id = Column(Integer, ForeignKey('influencer.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user_table.id'), nullable=False)
    influencer = relationship("Influencer", back_populates="watchlist")
    user = relationship("User", back_populates="watchlist")
