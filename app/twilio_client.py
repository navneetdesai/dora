import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from twilio.rest import Client

from .settings import settings


class TwilioClient:
    def __init__(self):
        self.client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)
        self.email = settings.EMAIL
        self.password = settings.APP_PASSWORD

    def send_text(self, message, to_number):
        self.client.messages.create(
            body=message, from_=settings.TWILIO_PHONE_NUMBER, to=str(to_number)
        )

    def send_email(self, subject, body, to_email):
        message = MIMEMultipart()
        message["From"] = self.email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(message)
