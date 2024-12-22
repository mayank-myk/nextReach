import random
from datetime import datetime


def get_campaign_id():
    return 'C' + datetime.now().strftime('%Y%m%d%H%M%S')


def get_user_id():
    return 'U' + datetime.now().strftime('%Y%m%d%H%M%S')


def get_influencer_id():
    return 'I' + datetime.now().strftime('%Y%m%d%H%M%S')


def get_influencer_metric_id():
    return 'M' + datetime.now().strftime('%Y%m%d%H%M%S')


def generate_otp() -> str:
    """Generate a 5-digit random OTP."""
    return str(random.randint(10000, 99999))
