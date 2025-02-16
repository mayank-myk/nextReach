from datetime import date

from pydantic import BaseModel


class NewSignupDump(BaseModel):
    login_date: str
    first_login_time: str
    phone_number: str
    user_status: str
