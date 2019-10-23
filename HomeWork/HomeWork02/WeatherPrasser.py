from datetime import datetime
import requests


class EasyWeather:

    import pyowm
    owm = pyowm.OWM('395c3de1a4a2308abca45267b8563f61')

    def __init__(self, city):
        self._city = city

    def get_weather(self):

        city = EasyWeather.owm.three_hours_forecast(self._city)
        weather = city.get_weather_at(datetime(int(input('Year: ')), int(input('Month: ')), int(input('Day: ')), int(input('Hour: ')), int(input('Minute: '))))
        return f'Weather at {self._city} is {weather.get_temperature("celsius")["temp"]} ℃'




class MediumWeather:

    def __init__(self, city, country):

        self._city = (requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&APPID=395c3de1a4a2308abca45267b8563f61').json())


    def print_weather(self):

        print(f'\t\t Weather at {self._city["name"]},{self._city["sys"].get("country")} is {self._city["weather"][0].get("main")}\n'
              f'Geo location: Longitude: {self._city["coord"].get("lon")} Latitude: {self._city["coord"].get("lat")}\n'
              f'Temperature: {self._city["main"].get("temp") - 273.15}\u2103 | Minimum: {self._city["main"].get("temp_min") - 273.15}\u2103 | Maximun {self._city["main"].get("temp_max") - 273.15}\u2103\n'
              f'Sunrise at: {datetime.fromtimestamp(self._city["sys"].get("sunrise"))} | Sunset at {datetime.fromtimestamp(self._city["sys"].get("sunset"))} UTC\n'
              )


kiev = MediumWeather('Antalya', 'TR')

kiev.print_weather()
