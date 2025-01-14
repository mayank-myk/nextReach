import requests

from app.enums.entity_type import EntityType
from app.enums.platform import Platform
from app.utils.logger import configure_logger

logger = configure_logger()
# INTERAKT_API_KEY = get_config("INTERAKT_API_KEY")
INTERAKT_API_KEY = "bGJEM09RRE0zTlp1bVplRURESUlQZnA3LXNYY3B4WExCOWJXMG1PZ0ZNazo="


def send_otp_via_whatsapp(phone_number: str, otp: str):
    API_URL = "https://api.interakt.ai/v1/public/message/"

    headers = {
        "Authorization": "Basic " + INTERAKT_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "countryCode": "+91",
        "phoneNumber": phone_number,
        "callbackData": "some text here",
        "type": "Template",
        "template": {
            "name": "verification",
            "languageCode": "en",
            "bodyValues": [
                str(otp)
            ],
            "buttonValues": {
                "1": [str(otp)]
            }
        }
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response code is 4xx/5xx

        # Check if message was successfully sent
        if response.status_code // 100 == 2:
            logger.info(f"OTP sent successfully to {phone_number}")
            return True
        else:
            logger.info(f"Failed to send OTP: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while sending OTP to {phone_number}. Error: {str(e)}")
        return False


def contact_us_notification_via_whatsapp(admin_phone_number: str, entity_type: EntityType, name: str,
                                         client_phone_number: str, email: str):
    API_URL = "https://api.interakt.ai/v1/public/message/"

    headers = {
        "Authorization": "Basic " + INTERAKT_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "countryCode": "+91",
        "phoneNumber": admin_phone_number,
        "callbackData": "some text here",
        "type": "Template",
        "template": {
            "name": "contact_us",
            "languageCode": "en",
            "bodyValues": [
                entity_type.value,
                name,
                client_phone_number,
                email
            ]
        }
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response code is 4xx/5xx

        # Check if message was successfully sent
        if response.status_code // 100 == 2:
            logger.info(f"Contact Us notification sent successfully to {admin_phone_number}")
            return True
        else:
            logger.info(f"Failed to send Contact Us notification: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(
            f"An error occurred while sending Contact Us notification to {admin_phone_number}. Error: {str(e)}")
        return False


def collab_request_user_notification_via_whatsapp(client_phone_number: str, date: str, influencer_name: str,
                                                  primary_platform: Platform, profile_link: str, content_price: int,
                                                  reach_price: int, followers: int, avg_views: int):
    API_URL = "https://api.interakt.ai/v1/public/message/"

    headers = {
        "Authorization": "Basic " + INTERAKT_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "countryCode": "+91",
        "phoneNumber": client_phone_number,
        "callbackData": "some text here",
        "type": "Template",
        "template": {
            "name": "collab_request_user",
            "languageCode": "en",
            "bodyValues": [
                date,
                influencer_name,
                primary_platform.value,
                profile_link,
                str(content_price),
                str(reach_price),
                str(followers),
                str(avg_views)
            ]
        }
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response code is 4xx/5xx

        # Check if message was successfully sent
        if response.status_code // 100 == 2:
            logger.info(f"Collab request user notification sent successfully to {client_phone_number}")
            return True
        else:
            logger.info(f"Failed to send Collab request user notification: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(
            f"An error occurred while sending Collab request user notification to {client_phone_number}. Error: {str(e)}")
        return False


def collab_request_admin_notification_via_whatsapp(admin_phone_number: str, date: str, campaign_id: str, client_id: str,
                                                   influencer_id: str, client_name: str, client_phone_number: str,
                                                   influencer_name: str, influencer_phone_number: str,
                                                   content_price: int, reach_price: int, followers: int,
                                                   avg_views: int):
    API_URL = "https://api.interakt.ai/v1/public/message/"

    headers = {
        "Authorization": "Basic " + INTERAKT_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "countryCode": "+91",
        "phoneNumber": admin_phone_number,
        "callbackData": "some text here",
        "type": "Template",
        "template": {
            "name": "collab_request_admin",
            "languageCode": "en",
            "bodyValues": [
                date,
                campaign_id,
                client_id,
                influencer_id,
                client_name,
                influencer_name,
                str(content_price),
                str(reach_price),
                str(followers),
                str(avg_views),
                client_phone_number,
                influencer_phone_number
            ]
        }
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response code is 4xx/5xx

        # Check if message was successfully sent
        if response.status_code // 100 == 2:
            logger.info(f"Collab request user notification sent successfully to {client_phone_number}")
            return True
        else:
            logger.info(f"Failed to send Collab request user notification: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(
            f"An error occurred while sending Collab request user notification to {client_phone_number}. Error: {str(e)}")
        return False
