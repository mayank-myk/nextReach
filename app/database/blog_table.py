import datetime

from sqlalchemy import Column, String, Integer, Date

from app.database.session import Base


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(Date, default=datetime.datetime.today, nullable=False)
    author = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
