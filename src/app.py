import schedule
import time
from storage.user_preferences import load_preferences
from src.scraper.weather_scraper import scrape_weather_data
from src.notifications.email_notification_smtp import send_weather_email
from src.notifications.sms_notification import send_weather_sms
from src.scraper.exceptions import WeatherScrapeError
from src.gui.gui import launch_gui


def job():
    """
        The job that runs at the scheduled intervals to send weather notifications.
        It fetches user preferences, scrapes weather data, and sends notifications accordingly.
    """

    preferences = load_preferences()
    city = preferences.get('city')
    email = preferences.get('to_email') if preferences.get('send_email') else None
    phone = preferences.get('to_phone') if preferences.get('send_sms') else None
    notification_preference = preferences.get('notification_preference', 'full-weather')

    try:
        weather_data = scrape_weather_data(city)
        print(f"Weather data for {city}: {weather_data}")

        if email:
            send_weather_email(email, city, weather_data, notification_preference)
            print(f"Email sent to {email} with weather data for {city}.")

        if phone:
            send_weather_sms(phone, city, weather_data, notification_preference)
            print(f"SMS sent to {phone} with weather data for {city}.")

    except WeatherScrapeError as e:
        print(f"Error: {e}")


def schedule_notifications():
    """
    Schedule the weather notifications based on user preferences.
    """
    preferences = load_preferences()
    frequency = preferences.get('frequency', 'daily')

    schedule.clear()

    if frequency == '10 minutes':
        schedule.every(10).minutes.do(job)
    elif frequency == 'hourly':
        schedule.every().hour.do(job)
    elif frequency == '6 hours':
        schedule.every(6).hours.do(job)
    elif frequency == 'daily':
        schedule.every().day.at("09:00").do(job)
    else:
        print(f"Unknown frequency: {frequency}. Defaulting to daily at 09:00.")
        schedule.every().day.at("09:00").do(job)


if __name__ == "__main__":

    # Run the application
    launch_gui(schedule_notifications)

    while True:
        schedule.run_pending()
        time_until_next_job = schedule.idle_seconds()

        if time_until_next_job > 0:
            time.sleep(time_until_next_job)
        else:
            time.sleep(1)
