class WeatherScrapeError(Exception):
    """Base class for other exceptions"""
    pass


class WeatherSearchError(WeatherScrapeError):
    """Raised when search results are not found"""
    pass


class WeatherPageNotFoundError(WeatherScrapeError):
    """Raised when a weather page link is not found"""
    pass


class WeatherDataNotFoundError(WeatherScrapeError):
    """Raised when weather data is missing from the weather page"""
    pass
