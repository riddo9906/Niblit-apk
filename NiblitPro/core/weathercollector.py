import requests

class WeatherCollector:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            return f"Weather in {city}: {data['weather'][0]['description']}, {data['main']['temp']}°C"
        return "Error fetching weather."