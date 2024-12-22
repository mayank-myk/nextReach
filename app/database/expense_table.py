from sqlalchemy import Column, Integer, String, DateTime, Enum, Date, CheckConstraint
import datetime

from app.database.session import Base
from app.models.expense_type import ExpenseType


class Expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_by = Column(String(255), nullable=False)
    last_updated_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                             nullable=False)
    type = Column(Enum(ExpenseType), nullable=False)  # Assuming ExpenseType is a valid Enum
    date = Column(Date, default=datetime.date.today, nullable=False)
    amount = Column(Integer, CheckConstraint('amount >= 1'), nullable=False)
    description = Column(String(255), nullable=False)
    mode_of_payment = Column(String(255), nullable=False)
    account_id = Column(String(255), nullable=False)
