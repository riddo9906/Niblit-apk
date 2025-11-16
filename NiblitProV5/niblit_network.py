# niblit_network.py - network helpers (monitor, weather, news)
import requests, threading, time, socket
from datetime import datetime

NETWORK_STATUS = {'connected': False, 'last_check': None, 'ip': None, 'latency_ms': None}

class NiblitNetwork:
    def __init__(self):
        self.test_url = 'https://www.google.com'
        self.running = True
        self._start_monitor()

    def check_connection(self, timeout=3):
        try:
            socket.create_connection(('8.8.8.8',53), timeout=timeout)
            NETWORK_STATUS['connected'] = True
            NETWORK_STATUS['ip'] = self.get_ip()
            NETWORK_STATUS['last_check'] = datetime.now().isoformat()
            return True
        except Exception:
            NETWORK_STATUS['connected'] = False
            NETWORK_STATUS['last_check'] = datetime.now().isoformat()
            return False

    def get_ip(self):
        try:
            return requests.get('https://api.ipify.org', timeout=4).text
        except Exception:
            return 'unavailable'

    def latency_test(self):
        import time
        start = time.time()
        try:
            requests.get(self.test_url, timeout=5)
            NETWORK_STATUS['latency_ms'] = round((time.time()-start)*1000,2)
        except Exception:
            NETWORK_STATUS['latency_ms'] = None

    def fetch_json(self, url):
        if not NETWORK_STATUS['connected'] and not self.check_connection():
            return {'error':'offline'}
        try:
            return requests.get(url, timeout=8).json()
        except Exception as e:
            return {'error': str(e)}

    def get_weather(self, lat=-33.93, lon=18.42):
        url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
        j = self.fetch_json(url)
        return j.get('current_weather', {'error':'unavailable'})

    def get_news(self, country='za', language='en'):
        url = f'https://newsdata.io/api/1/news?country={country}&language={language}'
        j = self.fetch_json(url)
        if isinstance(j, dict) and 'results' in j:
            return [a.get('title') for a in j['results'][:6]]
        return []

    def _monitor_loop(self):
        while self.running:
            try:
                self.check_connection()
                self.latency_test()
            except Exception as e:
                print("[NiblitNetwork] monitor error:", e)
            time.sleep(60)

    def _start_monitor(self):
        t = threading.Thread(target=self._monitor_loop, daemon=True)
        t.start()

    def shutdown(self):
        self.running = False

# instantiate
network = NiblitNetwork()

def init():
    print('[Niblit Network] Module initialized.')