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

        custom_weather_description = (f"Вот текущая сводка по погоде:\n"
                                      f"\"{info['weather'][0]['description'].lower()}\"\n"
                                      f"Текущая температура {int(info['main']['temp'] - 273)}, но ощущается как {int(info['main']['feels_like'] - 273)}, всё по Цельсию\n"
                                      f"Ветер около {info['wind']['speed']} метров в секунду\n"
                                      f"Влажность около {info['main']['humidity']} процентов \n")
        return custom_weather_description

    def get_weather_for_week(self, lat, lon):
        url = (f"http://api.openweathermap.org/data/2.5/forecast/daily?"
               f"lat={lat}"
               f"&lon={lon}&appid={self.__api_key}"
               f"cnt=7"
               f"&lang=ru"
               )
        result = requests.get(url=url)
        raw_info = result.text
        info = json.loads(raw_info)
        try:
            info_for_week = info["list"][:7]
        except KeyError:
            return "Так для такой инфы надо платную подписку на этот api иметь, вы чего..."
        custom_weather_description = ""
        for ind, info in enumerate(info_for_week):
            match ind:
                case 0:
                    day = "сегодня"
                case 1:
                    day = "завтра"
                case 2:
                    day = "послезавтра"
                case _:
                    day = f"{ind} день после текущего"

            custom_weather_description += (f"Вот текущая сводка по погоде на {day}:\n"
                                           f"\"{info['weather'][0]['description'].lower()}\" \n"
                                           f"Текущая температура {int(info['main']['temp'] - 273)},"
                                           f" но ощущается как {int(info['main']['feels_like'] - 273)}, всё по Цельсию\n"
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
