from core.realtime_collector import RealTimeCollector

class NewsModule:
    def __init__(self, api_key):
        self.collector = RealTimeCollector(api_key)

    def run(self, topic="technology"):
        return self.collector.get_news(topic)