import datetime
from sqlalchemy import Column, String, DateTime
from app.database.session import Base


class UserLogin(Base):
    __tablename__ = "user_login"

    # Primary Key
    id = Column(String(13), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    otp = Column(String(5), nullable=False)
    phone_number = Column(String(10), nullable=False)
