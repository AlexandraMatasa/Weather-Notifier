import requests
from bs4 import BeautifulSoup
from src.scraper.exceptions import WeatherScrapeError, WeatherSearchError, WeatherPageNotFoundError, WeatherDataNotFoundError


def get_search_weather_url(city: str) -> str:
    search_url = f"https://www.worldweatheronline.com/search-weather.aspx?q={city}"
    response = requests.get(search_url)

    if response.status_code != 200:
        raise WeatherSearchError(f"Failed to retrieve search results for {city} (Status code: {response.status_code})")

    soup = BeautifulSoup(response.content, 'html.parser')

    search_results = soup.find_all('li', class_='list-group-item')

    if not search_results:
        raise WeatherPageNotFoundError(f"No weather results found for {city}")

    for result in search_results:
        links = result.find_all('a', href=True)
        if links:
            return links[0]['href']
    raise WeatherPageNotFoundError(f"No valid weather links found for {city}")


def scrape_weather_data(city: str) -> tuple[str, str, str, str, str]:
    weather_page_url = get_search_weather_url(city)
    if not weather_page_url:
        raise WeatherPageNotFoundError(f"Could not find weather page for {city}")

    response = requests.get(weather_page_url)

    if response.status_code != 200:
        raise WeatherDataNotFoundError(f"Failed to retrieve weather data for {city} (Status code: {response.status_code})")

    soup = BeautifulSoup(response.content, 'html.parser')

    temperature_span = soup.find('span', class_='h1')
    temperature = temperature_span.text.strip() if temperature_span else None

    if not temperature:
        raise WeatherDataNotFoundError("Temperature data not found on the page")

    description_div = soup.find('div', class_="apixu_descr")
    description = description_div.text.strip() if description_div else None

    if not description:
        raise WeatherDataNotFoundError("Weather description not found on the page")

    wind_div = soup.find('div', string=lambda t: t and 'Wind' in t)
    wind = wind_div.text.strip() if wind_div else None

    if not wind:
        raise WeatherDataNotFoundError("Wind information not found on the page")

    precipitation_span = soup.find('span', string=lambda t: t and 'Precip' in t)
    precipitation = precipitation_span.text.strip() if precipitation_span else None

    if not precipitation:
        raise WeatherDataNotFoundError("Precipitation information not found on the page")

    pressure_div = soup.find('div', string=lambda t: t and 'Pressure' in t)
    pressure = pressure_div.text.strip() if pressure_div else None

    if not pressure:
        raise WeatherDataNotFoundError("Pressure information not found on the page")

    return temperature, description, wind, precipitation, pressure


# city = 'Grinties'
#
# try:
#     weather_data = scrape_weather_data(city)
#
#     if weather_data:
#         temperature, weather_description, wind, precipitation, pressure = weather_data
#
#         print(f"Temperature: {temperature}")
#         print(f"Condition: {weather_description}")
#         print(f"{wind}")
#         print(f"{precipitation}")
#         print(f"{pressure}")
#
# except WeatherScrapeError as e:
#     print(f"Error: {e}")
