from requests import HTTPError

from src.config import settings
from src.services.general import Client

WEATHER_API_KEY = settings.WEATHER_API_KEY


class CityWeatherApi:
    """
    Класс для работы с запросами сервиса api.openweathermap.org
    """

    def __init__(self):
        """
        Инициализирует класс
        """
        self.client = Client()
        self.base_url = 'https://api.openweathermap.org'

    def get_weather_url(self, city):
        """
        Генерирует url включая в него необходимые параметры
        Args:
            city: Город
        Returns:

        """

        url = f'{self.base_url}/data/2.5/weather'
        url += '?units=metric'
        url += '&q=' + city
        url += '&appid=' + WEATHER_API_KEY

        return url

    def get_weather_from_response(self, response):
        """
        Достает погоду из ответа
        Args:
            response: Ответ, пришедший с сервера
        Returns:

        """

        data = response.json()

        return data['main']['temp']

    def get_weather(self, city):
        """
        Делает запрос на получение погоды
        Args:
            city: Город
        Returns:

        """

        url = self.get_weather_url(city)
        r = self.client.send_request(method=Client.GET, url=url)

        if r is None:
            return None
        else:
            weather = self.get_weather_from_response(r)
            return weather

    def check_existing(self, city):
        """
        Проверяет наличие города
        Args:
            city: Название города
        Returns:

        """

        url = self.get_weather_url(city)

        try:
            self.client.send_request(method=Client.GET, url=url)
        except HTTPError:
            return False

        return True
