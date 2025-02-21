from typing import Optional

from pydantic import BaseModel


class NewSignupDump(BaseModel):
    login_date: str
    first_login_time: str
    phone_number: str
    user_status: str
    otp_sent_successfully: bool
    login_success: bool
    total_profile_visited: Optional[int]
