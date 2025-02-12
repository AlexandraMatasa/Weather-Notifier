from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

class TwilioSMS:
    ACCOUNT_SID =  os.getenv("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    FROM_PHONE = "+12676338595"

    @classmethod
    def send_sms(cls, to_phone: str, message: str):
        """
               Sends SMS with the message using Twilio.

               Args:
                   to_phone (str): Recipient phone number.
                   message (str): Message content.
        """
        client = Client(cls.ACCOUNT_SID, cls.AUTH_TOKEN)

        try:
            client.messages.create(
                body=message,
                from_=cls.FROM_PHONE,
                to=to_phone
            )
        except Exception as e:
            print(f"Failed to send SMS to {to_phone}: {e}")
