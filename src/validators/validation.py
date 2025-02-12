import re


class Validator:
    @staticmethod
    def validate_email(email: str) -> bool:
        email_pattern = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$'
        return bool(re.match(email_pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        phone_pattern = r'^\+[1-9][0-9]{0,2}[0-9]{10}$'
        return bool(re.match(phone_pattern, phone))

