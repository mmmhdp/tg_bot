import json

import requests


class WeatherApi:
    def __init__(self):
        self.__api_key = "fb4a7f380bf95bbc9ae7cdf8012dbfa1"

    def get_weather_by_lat_and_lon(self, lat, lon):
        url = (f"http://api.openweathermap.org/data/2.5/weather?"
               f"lat={lat}"
               f"&lon={lon}&appid={self.__api_key}"
               f"&lang=ru")
        result = requests.get(url=url)
        raw_info = result.text
        info = json.loads(raw_info)

        custom_weather_description = (f"Вот текущая сводка по погоде в {info['name']}:\n"
                                      f"\"{info['weather'][0]['description'].lower()}\"\n"
                                      f"Текущая температура {int(info['main']['temp'] - 273)}, но ощущается как {int(info['main']['feels_like'] - 273)}, всё по Цельсию\n"
                                      f"Ветер около {info['wind']['speed']} метров в секунду\n"
                                      f"Влажность около {info['main']['humidity']} процентов \n")
        return custom_weather_description

    def get_weather_by_city(self, city):
        city = city
        url = (f"http://api.openweathermap.org/geo/1.0/direct?"
               f"q={city}"
               f"&appid={self.__api_key}")
        result = requests.get(url=url)
        raw_info = result.text
        info = json.loads(raw_info)
        try:
            lat, lon = info[0]["lat"], info[0]["lon"]
        except IndexError:
            return "Что-то тут не так... Давайте попробуем ещё раз"
        return self.get_weather_by_lat_and_lon(lat, lon)
