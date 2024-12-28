import datetime

from sqlalchemy import Column, String, DateTime, Integer

from app.database.session import Base


class UserLogin(Base):
    __tablename__ = "user_login"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    otp = Column(String(5), nullable=False)
    phone_number = Column(String(10), nullable=False)
