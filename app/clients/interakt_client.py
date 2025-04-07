from datetime import datetime
from typing import Optional, List, Dict

import httpx
import requests

from app.enums.campaign_stage import CampaignStage
from app.enums.entity_type import EntityType
from app.enums.platform import Platform
from app.utils.converters import format_to_currency, format_to_views_charge, int_to_str_k, \
    campaign_stage_to_user_friendly_str, influencer_charge_string
from app.utils.logger import configure_logger

logger = configure_logger()
# INTERAKT_API_KEY = get_config("INTERAKT_API_KEY")
INTERAKT_API_KEY = "bGJEM09RRE0zTlp1bVplRURESUlQZnA3LXNYY3B4WExCOWJXMG1PZ0ZNazo="
ADMIN_PHONE_NUMBERS = ["7008680032", "7676604090", "9731923797", "6901030545"]
HEADERS = {
    "Authorization": "Basic " + INTERAKT_API_KEY,
    "Content-Type": "application/json"
}
API_URL = "https://api.interakt.ai/v1/public/message/"


def build_payload(phone_number: str, template_name: str, body_values: List[str],
                  button_values: Optional[List[str]]) -> Dict:
    """Builds the payload for the WhatsApp API."""
    if not button_values:
        return {
            "countryCode": "+91",
            "phoneNumber": phone_number,
            "callbackData": "some text here",
            "type": "Template",
            "template": {
                "name": template_name,
                "languageCode": "en",
                "bodyValues": body_values
            }
        }
    else:
        return {
            "countryCode": "+91",
            "phoneNumber": phone_number,
            "callbackData": "some text here",
            "type": "Template",
            "template": {
                "name": template_name,
                "languageCode": "en",
                "bodyValues": body_values,
                "buttonValues": {
                    "0": button_values
                }
            }
        }


def send_sync_whatsapp_message(phone_number: str, template_name: str, body_values: List[str], command: str,
                               button_values: Optional[List[str]] = None) -> bool:
    payload = build_payload(phone_number, template_name, body_values, button_values)

    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS, verify=False)
        response.raise_for_status()

        if response.status_code // 100 == 2:
            logger.info(f"{command} whatsapp message successfully sent to {phone_number}")
            return True
        else:
            logger.error(f"Failed to send {command} whatsapp message: {response.text}")
            return False
    except Exception as e:
        logger.error(
            f"An error occurred while sending {command} whatsapp message to {phone_number}. Error: {str(e)}")
        return False


async def send_async_whatsapp_message(phone_number: str, template_name: str, body_values: List[str],
                                      command: str, button_values: Optional[List[str]] = None) -> bool:
    """Sends a WhatsApp message using the Interakt API."""
    payload = build_payload(phone_number, template_name, body_values, button_values)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, json=payload, headers=HEADERS)
            response.raise_for_status()

            if response.status_code // 100 == 2:
                logger.info(f"{command} whatsapp message successfully sent to {phone_number}")
                return True
            else:
                logger.error(f"Failed to send {command} whatsapp message: {response.text}")
                return False
        except Exception as e:
            logger.error(
                f"An error occurred while sending {command} whatsapp message to {phone_number}. Error: {str(e)}")
            return False


def send_otp_via_whatsapp(phone_number: str, otp: str):
    """Synchronous OTP sending."""
    return send_sync_whatsapp_message(phone_number, "verification", [str(otp)], "User OTP", [str(otp)])


async def notify_admins(template_name: str, body_values: List[str], command: str):
    """Sends a notification to all admin phone numbers."""
    for admin_phone_number in ADMIN_PHONE_NUMBERS:
        await send_async_whatsapp_message(admin_phone_number, template_name, body_values, command)


async def contact_us_notification_via_whatsapp(entity_type: EntityType, name: str,
                                               client_phone_number: str, email: Optional[str], message: Optional[str]):
    await notify_admins(
        "contact_us",
        [
            entity_type.value,
            name,
            client_phone_number,
            email or "Null",
            message or "Null",
            datetime.now().strftime("%b %d, %Y %I:%M %p")
        ], "Contact Us Admin"
    )


async def collab_request_user_notification_via_whatsapp(client_phone_number: str, date: str, influencer_name: str,
                                                        primary_platform: Platform, deliverables: list,
                                                        profile_link: str, fixed_price: int, followers: int,
                                                        avg_views: int, campaign_id: int):
    await send_async_whatsapp_message(
        client_phone_number,
        "collab_request_raised_user",
        [
            date,
            influencer_name,
            primary_platform.value,
            profile_link,
            influencer_charge_string(fixed_price, deliverables),
            int_to_str_k(followers),
            int_to_str_k(avg_views)
        ],
        "Collab Request User",
        [str(campaign_id)]
    )


async def collab_request_admin_notification_via_whatsapp(date: str, campaign_id: str, client_id: str,
                                                         influencer_id: str, client_name: Optional[str],
                                                         client_phone_number: str, influencer_name: str,
                                                         influencer_phone_number: str, fixed_price: int):
    await notify_admins(
        "collab_request_admin",
        [
            date,
            campaign_id,
            client_id,
            client_name if client_name else "",
            client_phone_number,
            influencer_id,
            influencer_name,
            influencer_phone_number,
            format_to_currency(fixed_price)
        ],
        "Collab Request Admin"
    )


def influencer_contact_detail_via_whatsapp(phone_number: str, influencer_name: str, profile_link: str,
                                           influencer_phone_number: str, influencer_email: str,
                                           fixed_price: int, deliverables: list):
    return send_sync_whatsapp_message(phone_number, "influencer_contact_detail1", [
        influencer_name,
        profile_link,
        influencer_phone_number,
        influencer_email or "Not available",
        influencer_charge_string(fixed_price, deliverables)
    ], "Influencer Contact Detail")


async def campaign_update_notification_via_whatsapp(campaign_id: int, client_phone_number: str,
                                                    influencer_name: str,
                                                    campaign_status: CampaignStage):
    await send_async_whatsapp_message(
        client_phone_number,
        "campaign_stage_update_client",
        [influencer_name, campaign_stage_to_user_friendly_str(campaign_status)],
        "Campaign Update User",
        [str(campaign_id)]
    )


async def campaign_draft_approved_notification_via_whatsapp(client_phone_number: str, influencer_name: str,
                                                            content_charge: int, upi_id: Optional[str]):
    await send_async_whatsapp_message(
        client_phone_number,
        "payment_request_content",
        [
            influencer_name,
            format_to_currency(content_charge),
            upi_id or "NOT_FOUND"
        ],
        "Campaign draft approved user"
    )


async def campaign_day2_billing_notification_via_whatsapp(client_phone_number: str, influencer_name: str,
                                                          views: int, reach_price: int, upi_id: Optional[str]):
    await send_async_whatsapp_message(
        client_phone_number,
        "payment_request_day2",
        [
            influencer_name,
            format_to_currency(views),
            format_to_views_charge(reach_price),
            format_to_currency((views * reach_price) // 1000),
            upi_id or "NOT_FOUND"
        ],
        "Campaign day2 billing user"
    )


async def campaign_day8_billing_notification_via_whatsapp(client_phone_number: str, influencer_name: str,
                                                          views: int, reach_price: int, upi_id: Optional[str]):
    await send_async_whatsapp_message(
        client_phone_number,
        "payment_request_day8",
        [
            influencer_name,
            format_to_currency(views),
            format_to_views_charge(reach_price),
            format_to_currency((views * reach_price) // 1000),
            upi_id or "NOT_FOUND"
        ],
        "Campaign day8 billing user"
    )
