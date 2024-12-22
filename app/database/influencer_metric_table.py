import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.session import Base


class InfluencerMetric(Base):
    __tablename__ = "influencer_metric"

    # Primary Key
    id = Column(String(13), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                             nullable=False)
    created_by = Column(String(255), nullable=False)
    last_updated_by = Column(String(255), nullable=False)

    # Foreign Key to Influencer
    influencer_id = Column(String(13), ForeignKey('influencer.id'), nullable=False)

    # Social media data
    insta_followers = Column(Integer, CheckConstraint('insta_followers >= 0'), default=0)
    insta_city_1 = Column(Integer, CheckConstraint('insta_city_1 >= 0'), default=0)
    insta_city_pc_1 = Column(Integer, CheckConstraint('insta_city_pc_1 >= 0'), default=0)
    insta_city_2 = Column(Integer, CheckConstraint('insta_city_2 >= 0'), default=0)
    insta_city_pc_2 = Column(Integer, CheckConstraint('insta_city_pc_2 >= 0'), default=0)
    insta_city_3 = Column(Integer, CheckConstraint('insta_city_3 >= 0'), default=0)
    insta_city_pc_3 = Column(Integer, CheckConstraint('insta_city_pc_3 >= 0'), default=0)
    insta_age_13_to_17 = Column(Integer, CheckConstraint('insta_age_13_to_17 >= 0'), default=0)
    insta_age_18_to_24 = Column(Integer, CheckConstraint('insta_age_18_to_24 >= 0'), default=0)
    insta_age_25_to_34 = Column(Integer, CheckConstraint('insta_age_25_to_34 >= 0'), default=0)
    insta_age_35_to_44 = Column(Integer, CheckConstraint('insta_age_35_to_44 >= 0'), default=0)
    insta_age_45_to_54 = Column(Integer, CheckConstraint('insta_age_45_to_54 >= 0'), default=0)
    insta_age_55 = Column(Integer, CheckConstraint('insta_age_55 >= 0'), default=0)
    insta_men_follower_pc = Column(Integer, CheckConstraint('insta_men_follower_pc >= 0'), default=0)
    insta_women_follower_pc = Column(Integer, CheckConstraint('insta_women_follower_pc >= 0'), default=0)
    insta_avg_views = Column(Integer, CheckConstraint('insta_avg_views >= 0'), default=0)
    insta_max_views = Column(Integer, CheckConstraint('insta_max_views >= 0'), default=0)
    insta_min_views = Column(Integer, CheckConstraint('insta_min_views >= 0'), default=0)
    insta_spread = Column(Integer, CheckConstraint('insta_spread >= 0'), default=0)
    insta_avg_likes = Column(Integer, CheckConstraint('insta_avg_likes >= 0'), default=0)
    insta_avg_comments = Column(Integer, CheckConstraint('insta_avg_comments >= 0'), default=0)
    insta_avg_shares = Column(Integer, CheckConstraint('insta_avg_shares >= 0'), default=0)
    insta_engagement_rate = Column(Integer, CheckConstraint('insta_engagement_rate >= 0'), default=0)

    yt_followers = Column(Integer, CheckConstraint('yt_followers >= 0'), default=0)
    yt_city_1 = Column(Integer, CheckConstraint('yt_city_1 >= 0'), default=0)
    yt_city_pc_1 = Column(Integer, CheckConstraint('yt_city_pc_1 >= 0'), default=0)
    yt_city_2 = Column(Integer, CheckConstraint('yt_city_2 >= 0'), default=0)
    yt_city_pc_2 = Column(Integer, CheckConstraint('yt_city_pc_2 >= 0'), default=0)
    yt_city_3 = Column(Integer, CheckConstraint('yt_city_3 >= 0'), default=0)
    yt_city_pc_3 = Column(Integer, CheckConstraint('yt_city_pc_3 >= 0'), default=0)
    yt_avg_views = Column(Integer, CheckConstraint('yt_avg_views >= 0'), default=0)
    yt_max_views = Column(Integer, CheckConstraint('yt_max_views >= 0'), default=0)
    yt_min_views = Column(Integer, CheckConstraint('yt_min_views >= 0'), default=0)
    yt_spread = Column(Integer, CheckConstraint('yt_spread >= 0'), default=0)
    yt_avg_likes = Column(Integer, CheckConstraint('yt_avg_likes >= 0'), default=0)
    yt_avg_comments = Column(Integer, CheckConstraint('yt_avg_comments >= 0'), default=0)
    yt_avg_shares = Column(Integer, CheckConstraint('yt_avg_shares >= 0'), default=0)
    yt_engagement_rate = Column(Integer, CheckConstraint('yt_engagement_rate >= 0'), default=0)

    fb_followers = Column(Integer, CheckConstraint('fb_followers >= 0'), default=0)
    fb_city_1 = Column(Integer, CheckConstraint('fb_city_1 >= 0'), default=0)
    fb_city_pc_1 = Column(Integer, CheckConstraint('fb_city_pc_1 >= 0'), default=0)
    fb_city_2 = Column(Integer, CheckConstraint('fb_city_2 >= 0'), default=0)
    fb_city_pc_2 = Column(Integer, CheckConstraint('fb_city_pc_2 >= 0'), default=0)
    fb_city_3 = Column(Integer, CheckConstraint('fb_city_3 >= 0'), default=0)
    fb_city_pc_3 = Column(Integer, CheckConstraint('fb_city_pc_3 >= 0'), default=0)
    fb_avg_views = Column(Integer, CheckConstraint('fb_avg_views >= 0'), default=0)
    fb_max_views = Column(Integer, CheckConstraint('fb_max_views >= 0'), default=0)
    fb_min_views = Column(Integer, CheckConstraint('fb_min_views >= 0'), default=0)
    fb_spread = Column(Integer, CheckConstraint('fb_spread >= 0'), default=0)
    fb_avg_likes = Column(Integer, CheckConstraint('fb_avg_likes >= 0'), default=0)
    fb_avg_comments = Column(Integer, CheckConstraint('fb_avg_comments >= 0'), default=0)
    fb_avg_shares = Column(Integer, CheckConstraint('fb_avg_shares >= 0'), default=0)
    fb_engagement_rate = Column(Integer, CheckConstraint('fb_engagement_rate >= 0'), default=0)

    # Relationship to Influencer
    influencer = relationship("Influencer", back_populates="influencer_metric")
