import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, CheckConstraint, Float
from sqlalchemy.orm import relationship

from app.database.session import Base


class InfluencerFbMetric(Base):
    __tablename__ = "influencer_fb_metric"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                             nullable=False)
    created_by = Column(String(255), nullable=False)
    last_updated_by = Column(String(255), nullable=False)

    # Foreign Key to Influencer
    influencer_id = Column(Integer, ForeignKey('influencer.id'), nullable=False, index=True)

    username = Column(String(255), nullable=False)
    profile_link = Column(String(1000), nullable=False)
    followers = Column(Integer, CheckConstraint('followers >= 0'), nullable=True)
    avg_views = Column(Integer, CheckConstraint('avg_views >= 0'), nullable=True)
    max_views = Column(Integer, CheckConstraint('max_views >= 0'), nullable=True)
    min_views = Column(Integer, CheckConstraint('min_views >= 0'), nullable=True)
    consistency_score = Column(Integer, CheckConstraint('consistency_score >= 0'), nullable=True)
    avg_likes = Column(Integer, CheckConstraint('avg_likes >= 0'), nullable=True)
    avg_comments = Column(Integer, CheckConstraint('avg_comments >= 0'), nullable=True)
    avg_shares = Column(Integer, CheckConstraint('avg_shares >= 0'), nullable=True)
    engagement_rate = Column(Float, CheckConstraint('engagement_rate >= 0'), nullable=True)

    city_1 = Column(String(255), nullable=True)
    city_pc_1 = Column(Integer, CheckConstraint('city_pc_1 >= 0'), nullable=True)
    city_2 = Column(String(255), nullable=True)
    city_pc_2 = Column(Integer, CheckConstraint('city_pc_2 >= 0'), nullable=True)
    city_3 = Column(String(255), nullable=True)
    city_pc_3 = Column(Integer, CheckConstraint('city_pc_3 >= 0'), nullable=True)
    age_13_to_17 = Column(Integer, CheckConstraint('age_13_to_17 >= 0'), nullable=True)
    age_18_to_24 = Column(Integer, CheckConstraint('age_18_to_24 >= 0'), nullable=True)
    age_25_to_34 = Column(Integer, CheckConstraint('age_25_to_34 >= 0'), nullable=True)
    age_35_to_44 = Column(Integer, CheckConstraint('age_35_to_44 >= 0'), nullable=True)
    age_45_to_54 = Column(Integer, CheckConstraint('age_45_to_54 >= 0'), nullable=True)
    age_55 = Column(Integer, CheckConstraint('age_55 >= 0'), nullable=True)
    men_follower_pc = Column(Integer, CheckConstraint('men_follower_pc >= 0'), nullable=True)
    women_follower_pc = Column(Integer, CheckConstraint('women_follower_pc >= 0'), nullable=True)

    # Relationship to Influencer
    influencer = relationship("Influencer", back_populates="influencer_fb_metric")
