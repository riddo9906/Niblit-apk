from core.weathercollector import WeatherCollector

class WeatherModule:
    def __init__(self, api_key):
        self.collector = WeatherCollector(api_key)

    def run(self, city):
        return self.collector.get_weather(city)