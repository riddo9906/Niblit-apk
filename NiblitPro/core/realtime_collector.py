import requests

class RealTimeCollector:
    def __init__(self, news_api_key):
        self.news_api_key = news_api_key

    def get_news(self, topic="technology"):
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={self.news_api_key}"
        r = requests.get(url)
        if r.status_code == 200:
            articles = r.json().get("articles", [])
            if articles:
                return f"News: {articles[0]['title']} - {articles[0]['url']}"
            return "No news found."
        return "Error fetching news."