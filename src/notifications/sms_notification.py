from src.libs.twilio_sms import TwilioSMS


def send_weather_sms(to_phone: str, city: str, weather_data: tuple, preference: str):
    """
        Sends weather data via SMS using Twilio based on user preferences.

        Args:
            to_phone (str): Recipient phone number.
            city (str): City for the weather update.
            weather_data (tuple): Tuple containing weather information.
            preference (str): "umbrella-only" for umbrella reminders or "full-weather" for full weather updates.
    """
    temperature, description, wind, precipitation, pressure = weather_data

    rain_keywords = ["rain", "drizzle", "shower", "storm"]
    precipitation_threshold = 0.5

    is_rain = any(keyword in description.lower() for keyword in rain_keywords)

    try:
        precipitation_value = float(precipitation.split()[1])
    except ValueError:
        precipitation_value = 0

    if is_rain or precipitation_value > precipitation_threshold:
        message = f"Don't forget your umbrella! It looks like rain in {city}.\n\n"

        if preference == "umbrella-only":
            TwilioSMS.send_sms(to_phone, message)
            return
    else:
        message = f"No rain expected in {city}."

    if preference == "full-weather":
        message += f"Here's the full weather update:\n\n"
        message += f"Temperature: {temperature}\n"
        message += f"Condition: {description}\n"
        message += f"{wind}\n"
        message += f"{precipitation}\n"
        message += f"{pressure}\n"

    TwilioSMS.send_sms(to_phone, message)