import io
import json
import uuid
from typing import Optional

import boto3

from simpl_utils.clients.s3 import S3
from simpl_utils.config import aws_default_bucket
from app.utils.logger import configure_logger
from app.utils.config import get_config

logger = configure_logger()


class S3Manager:

    def __init__(self):
        self.s3 = S3()

    def get_user_profile(self, user_id: str) -> UserProfile:

        login_record = self.login_repository.get_otp_by_phone_number(phone_number=phone_number)
        if login_record and (datetime.now() - login_record.created_at).seconds <= 600:
            return GenericResponse(success=False, error_code=None,
                                   error_message="OTP has been already sent, its valid for 10mins.")

        otp = random.randint(100000, 999999)

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = get_config("BREVO_API_KEY")

        get_config("OTP_MESSAGE")

        api_instance = sib_api_v3_sdk.TransactionalSMSApi(sib_api_v3_sdk.ApiClient(configuration))
        send_transac_sms = sib_api_v3_sdk.SendTransacSms(sender="HappyScreen", recipient="91" + phone_number,
                                                         content=get_config("OTP_MESSAGE").format(str(otp)),
                                                         type="transactional",
                                                         web_url=None)

        try:
            api_response = api_instance.send_transac_sms(send_transac_sms)
            pprint(api_response)
            _log.info("OTP has been sent to phone number {}".format(phone_number))

            success = self.login_repository.save_otp_and_phone_number(otp=str(otp), phone_number=phone_number)
            if success:
                return GenericResponse(success=True, error_code=None,
                                       error_message="OTP has been sent to your registered mobile number")
            else:
                return GenericResponse(success=False, error_code=None,
                                       error_message="Unable to save generated OTP")

        except ApiException as e:
            _log.error("Exception when calling TransactionalSMSApi->send_transac_sms: %s\n" % e)
            return GenericResponse(success=False, error_code=None, error_message="Unable to send OTP")

    def update_user_profile(self, profile: ProfileUpdate, user_id: str) -> GenericResponse:

        login_record = self.login_repository.get_otp_by_phone_number(phone_number=phone_number)
        if login_record and (datetime.now() - login_record.created_at).seconds <= 600:
            return GenericResponse(success=False, error_code=None,
                                   error_message="OTP has been already sent, its valid for 10mins.")

        otp = random.randint(100000, 999999)

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = get_config("BREVO_API_KEY")

        get_config("OTP_MESSAGE")

        api_instance = sib_api_v3_sdk.TransactionalSMSApi(sib_api_v3_sdk.ApiClient(configuration))
        send_transac_sms = sib_api_v3_sdk.SendTransacSms(sender="HappyScreen", recipient="91" + phone_number,
                                                         content=get_config("OTP_MESSAGE").format(str(otp)),
                                                         type="transactional",
                                                         web_url=None)

        try:
            api_response = api_instance.send_transac_sms(send_transac_sms)
            pprint(api_response)
            _log.info("OTP has been sent to phone number {}".format(phone_number))

            success = self.login_repository.save_otp_and_phone_number(otp=str(otp), phone_number=phone_number)
            if success:
                return GenericResponse(success=True, error_code=None,
                                       error_message="OTP has been sent to your registered mobile number")
            else:
                return GenericResponse(success=False, error_code=None,
                                       error_message="Unable to save generated OTP")

        except ApiException as e:
            _log.error("Exception when calling TransactionalSMSApi->send_transac_sms: %s\n" % e)
            return GenericResponse(success=False, error_code=None, error_message="Unable to send OTP")

    def send_otp_through_whatsapp(self, phone_number: str) -> GenericResponse:

        configuration = sib_api_v3_sdk.Configuration()
        key = get_config("BREVO_API_KEY")
        sender_number = get_config("SENDER_NUMBER")
        configuration.api_key['api-key'] = key

        api_instance = sib_api_v3_sdk.TransactionalWhatsAppApi(sib_api_v3_sdk.ApiClient(configuration))
        send_transac_whatsapp_message = sib_api_v3_sdk.SendWhatsappMessage(sender_number=sender_number,
                                                                           contact_numbers=["+91" + phone_number],
                                                                           text="Please use this OTP to update your "
                                                                                "booking, from "
                                                                                "https://www.thehappyscreens.in/")

        try:
            api_response = api_instance.send_whatsapp_message(send_transac_whatsapp_message)
            pprint(api_response)
        except ApiException as e:
            _log.error("Exception when calling TransactionalWhatsappApi->send_transac_sms: %s\n" % e)

        _log.info("OTP has been sent to phone number {}".format(phone_number))
