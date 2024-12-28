import requests

from app.utils.logger import configure_logger

logger = configure_logger()
API_KEY = "your_interakt_api_key"


def send_otp_via_whatsapp(phone_number: str, otp: str):
    API_URL = "https://api.interakt.ai/v1/public/message/"

    headers = {
        "Authorization": f"Basic {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "countryCode": "+91",
        "phoneNumber": phone_number,
        # "campaignId": "YOUR_CAMPAIGN_ID",
        # "callbackData": "some text here",
        "type": "Template",
        "template": {
            "name": "template_name_here",
            "languageCode": "en",
            "bodyValues": [
                str(otp)
            ]
        }
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response code is 4xx/5xx

        # Check if message was successfully sent
        if response.status_code == 200:
            logger.info(f"OTP sent successfully to {phone_number}")
            return True
        else:
            logger.info(f"Failed to send OTP: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while sending OTP to {phone_number} . Error: {str(e)}")
        return False
