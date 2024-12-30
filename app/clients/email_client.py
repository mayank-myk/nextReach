import tempfile
from pprint import pprint

import pdfkit
import sib_api_v3_sdk
from jinja2 import Template

from app.utils.config import get_config
from app.utils.logger import configure_logger

logger = configure_logger()


def send_booking_bill(pdf_output_url: str, receiver_email: str) -> bool:
    try:
        sender_email = get_config("EMAIL_SENDER_EMAIL")
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = get_config("BREVO_API_KEY")
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        sender = {"email": sender_email}
        html_content = """\
            <html>
              <body>
                <p>
                Hi,<br>
                Please find the attached booking GST Invoice.<br><br>

                Thanks<br>
                The Happy Screens<br>
              </body>
            </html>
            """
        subject = "Please find the attached booking invoice, from The Happy Screens"
        to_field = [
            {
                "email": receiver_email
            }
        ]

        smtp_template = sib_api_v3_sdk.SendSmtpEmail(sender=sender, html_content=html_content,
                                                     subject=subject, to=to_field, reply_to=sender,
                                                     attachment=pdf_output_url)

        api_response = api_instance.send_transac_email(smtp_template)
        _log.info('Bill has been sent to' + receiver_email)
        pprint(api_response)
        return True

    except Exception as e:
        _log.error("Exception when calling SMTPApi->post_email: %s\n" % e)
        return False


def generate_bill(self, campaign_id: str) -> GenericResponse:
    booking = self.booking_repository.get_booking_from_booking_id(booking_id=booking_id)
    if booking:
        try:
            with open('invoice_format.html', 'r') as file:
                content = file.read()
                template = Template(content)
                base_price = booking.total_price // 1.18
                tax = booking.total_price - base_price
                rendered_template = template.render(name=booking.booking_name, phone_number=booking.phone_number,
                                                    email=booking.email,
                                                    date=booking.booking_date.strftime("%b %d, %Y"),
                                                    total_amount=booking.total_price, tax=tax / 2,
                                                    base_price=base_price)

                pdf_output_path = tempfile.TemporaryFile()
                pdfkit.from_string(rendered_template, pdf_output_path)
                pdf_output_url = upload_bill(pdf_output_path)

                send_booking_bill(pdf_output_url, booking.email)
                _log.info(f"PDF generated at {pdf_output_path} and saved at {pdf_output_url}")

            return GenericResponse(success=True, error_code=None, error_message=None)
        except Exception as e:
            return GenericResponse(success=False, error_code=None,
                                   error_message="Exception while generating the Invoice")

    else:
        return GenericResponse(success=False, error_code=None,
                               error_message="No successful booking found for this booking_id")


def send_booking_email_for_free(booking: Booking) -> bool:
    receiver_email = booking.email

    try:
        # Configuration
        port = get_config("EMAIL_PORT")
        smtp_server = get_config("EMAIL_HOST")
        login = get_config("EMAIL_HOST_USER")
        password = get_config("EMAIL_HOST_PASSWORD")
        sender_email = get_config("EMAIL_SENDER_EMAIL")

        # Email content
        subject = "Booking confirmation with The Happy Screens"
        html = """\
        <html>
          <body>
            <p>Hi,<br>
            This is a <b>data</b> email without an attachment sent using <a href="https://www.python.org">Python</a>.</p>
          </body>
        </html>
        """

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach the HTML part
        message.attach(MIMEText(html, "html"))

        # Send the email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        _log.info('Booking email has been sent successfully to' + receiver_email)
        return True
    except Exception as e:
        _log.error('Error while sending booking email to ' + receiver_email, e)
        return False


def send_booking_email(booking: Booking) -> bool:
    try:
        sender_email = get_config("EMAIL_SENDER_EMAIL")
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = get_config("BREVO_API_KEY")
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        receiver_email = booking.email
        sender = {"email": sender_email}
        html_content = """\
        <html>
          <body>
            <p>Hi,<br>
            This is a <b>data</b> email without an attachment sent using <a href="https://www.python.org">Python</a>.</p>
          </body>
        </html>
        """
        subject = "Thanks for booking with The Happy Screens"
        to_field = [
            {
                "email": receiver_email,
                "name": booking.booking_name
            }
        ]

        smtp_template = sib_api_v3_sdk.SendSmtpEmail(sender=sender, html_content=html_content,
                                                     subject=subject, to=to_field, reply_to=sender,
                                                     )

        api_response = api_instance.send_transac_email(smtp_template)
        pprint(api_response)
        _log.info('Email has been sent to' + receiver_email)
        return True

    except Exception as e:
        _log.error("Exception when calling SMTPApi->post_email: %s\n" % e)
        return False
