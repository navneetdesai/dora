# Dora: Alert Management System
[![Build](https://github.com/navneetdesai/dora/actions/workflows/build.yml/badge.svg)](https://github.com/navneetdesai/dora/actions/workflows/build.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.96.0-blue)](https://fastapi.tiangolo.com/)
[![Twilio](https://img.shields.io/badge/Twilio-8.2.2-blue)](https://www.twilio.com/)
[![smtplib](https://img.shields.io/badge/smtplib-built--in-orange)](https://docs.python.org/3/library/smtplib.html)
[![pytest](https://img.shields.io/badge/pytest-7.3.2-green)](https://pytest.org/)
[![black](https://img.shields.io/badge/black-23.3.0-black)](https://black.readthedocs.io/)

Dora is a comprehensive alert management system built with FastAPI that helps businesses and organizations streamline their communication and notification processes. It provides user registration and login functionality, allowing users to securely access the system and manage their alerts. With Dora, you can effectively send alerts to subscribers based on their location, leveraging Twilio for text message notifications and the `smtplib` library for email notifications.
Dora can benefit groups like 🚨 **Emergency Services and Public Safety Agencies**, for critical alerts, public health advisories, and weather warnings.

## Key Features

🔒 **User Registration and Login:** Create accounts and securely log in to the system.

📍 **Location-Based Alerts:** Send targeted alerts to subscribers based on their specified location, ensuring timely and relevant communication.

📱 **Twilio Integration:** Seamlessly integrate with Twilio to trigger text messages as an alert delivery method.

📧 **Email Notifications:** Utilize the power of the `smtplib` library to send email messages as part of the alerting mechanism.

## API Documentation
The API documentation is available at http://localhost:8000/docs once the server is running.



## Installation
1. Clone the repository
```bash
git clone git@github.com:navneetdesai/dora.git
cd dora # change directory
poetry install # install dependencies
# Setup the configuration show below
poetry run uvicorn app.main:app --reload # run the app
```
Once the server is running, you can access the API documentation at http://localhost:8000/docs to explore the available endpoints and interact with the system.


## Configuration
1. Create a `.env` file in the root directory by copying .env-example (or rename .env-example to .env)
2. Create a twilio account and get the following values:
    - TWILIO_ACCOUNT_SID
    - TWILIO_AUTH_TOKEN
    - TWILIO_PHONE_NUMBER
3. Create a gmail account and get the email id and app password.
4. Update the environment variables in `.env` with your own values


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to submit a pull request or open an issue on the GitHub repository.





