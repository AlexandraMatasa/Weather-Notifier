import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class SMTPMail:
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    @classmethod
    def send_email(cls, to_email: str, subject: str, body: str):
        """
        Sends an email using SMTP.

        Args:
            to_email (str): Recipient's email address.
            subject (str): Subject of the email.
            body (str): Body content of the email.
        """
        msg = MIMEMultipart()
        msg['From'] = cls.SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(cls.SMTP_SERVER, cls.SMTP_PORT)
            server.starttls()
            server.login(cls.SMTP_USER, cls.SMTP_PASSWORD)
            server.sendmail(cls.SMTP_USER, to_email, msg.as_string())
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()
