import datetime

from sqlalchemy import Column, String, Integer, Date

from app.database.session import Base


class SuccessStory(Base):
    __tablename__ = "success_story"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(Date, default=datetime.datetime.today, nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    group_name = Column(String(255), nullable=False)
    tag1 = Column(String(255), nullable=False)
    tag2 = Column(String(255), nullable=False)
    business_image = Column(String(255), nullable=False)
    influencer_image = Column(String(255), nullable=False)
