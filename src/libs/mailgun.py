import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Mailgun:
    MAILGUN_API_URL = os.getenv("MAILGUN_API_URL")
    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")

    FROM_NAME = os.getenv("FROM_NAME")
    FROM_EMAIL = os.getenv("FROM_EMAIL")

    @classmethod
    def send_email(cls, to_emails, subject, content):
        """Send emails via Mailgun"""

        response = requests.post(
            cls.MAILGUN_API_URL,
            auth=('api', cls.MAILGUN_API_KEY),
            data={
                'from': f'{cls.FROM_NAME} <{cls.FROM_EMAIL}>',
                'to': to_emails,
                'subject': subject,
                'text': content
            }
        )

        if response.status_code == 200:
            print(f"Email sent to {to_emails}")
        else:
            print(f"Failed to send email: {response.status_code}, {response.text}")

