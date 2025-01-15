import datetime

from sqlalchemy import Column, String, Integer, Date

from app.database.session import Base


class AcademyVideo(Base):
    __tablename__ = "academy_video"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(Date, default=datetime.datetime.today, nullable=False)
    yt_link = Column(String(1000), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    tag1 = Column(String(255), nullable=False)
    tag2 = Column(String(255), nullable=False)
    tag3 = Column(String(255), nullable=False)
    tag4 = Column(String(255), nullable=False)
