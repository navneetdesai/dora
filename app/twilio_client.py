import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

from .settings import settings


class TwilioClient:
    def __init__(self):
        self.client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)
        self.email = settings.EMAIL
        self.password = settings.PASSWORD

    def send_text(self, message, to_number):
        self.client.messages.create(
            body=message, from_=settings.TWILIO_PHONE_NUMBER, to=str(to_number)
        )

    def send_email(self, body, to_email):
        message = MIMEMultipart()
        message["From"] = self.email
        message["To"] = to_email
        message["Subject"] = "Alert from Dora"
        message.attach(MIMEText(body, "plain"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(message)
