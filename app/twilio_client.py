"""
Handles SMS and Email alerts
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from twilio.rest import Client

from .settings import settings


class TwilioClient:
    """
    Client to send SMS and Email alerts
    """

    def __init__(self):
        """
        Setup Twilio client
        """
        self.settings = settings()
        self.client = Client(self.settings.TWILIO_SID, self.settings.TWILIO_TOKEN)
        self.email = self.settings.EMAIL
        self.password = self.settings.APP_PASSWORD

    def send_text(self, message, to_number):
        """
        Send SMS to the given number
        :param message: Message to send
        :param to_number: Number to send SMS to
        :return: None
        """
        self.client.messages.create(
            body=message, from_=self.settings.TWILIO_PHONE_NUMBER, to=str(to_number)
        )

    def send_email(self, subject, body, to_email):
        """
        Send email to the given email address
        :param subject: Subject of the email
        :param body: Body of the email
        :param to_email: email address to send email to
        :return:
        """
        message = MIMEMultipart()  # set up the parameters
        message["From"] = self.email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.email, self.password)  # email login
            server.send_message(message)
