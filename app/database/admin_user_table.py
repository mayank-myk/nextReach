import datetime

from sqlalchemy import Column, String, Enum, Integer, DateTime

from app.database.session import Base
from app.enums.admin_type import AdminType


class AdminUser(Base):
    __tablename__ = 'admin_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                             nullable=False)
    created_by = Column(String(255), nullable=False)
    admin_id = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    admin_type = Column(Enum(AdminType), default=AdminType.SUPER_ADMIN, nullable=False)
