import json
import os

PREFERENCES_FILE = "user_preferences.json"


def save_preferences(frequency, send_email, send_sms, to_email, to_phone, city, notification_preference):
    """
        Save the user's notification preferences to a JSON file.
    """
    preferences = {
        "frequency": frequency,
        "send_email": send_email,
        "send_sms": send_sms,
        "to_email": to_email,
        "to_phone": to_phone,
        "city": city,
        "notification_preference": notification_preference
    }

    with open(PREFERENCES_FILE, "w") as file:
        json.dump(preferences, file, indent=4)


def load_preferences():
    """
        Load the user's notification preferences from a JSON file.
        If no preferences file is found, return None.
    """
    if not os.path.exists(PREFERENCES_FILE):
        return None

    with open(PREFERENCES_FILE, "r") as file:
        return json.load(file)
