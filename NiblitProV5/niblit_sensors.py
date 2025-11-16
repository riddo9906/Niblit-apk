# niblit_sensors.py - simple sensor bridge with safe fallbacks
import threading, time, random

SENSOR_STATUS = {'gps':None, 'camera':False, 'microphone':False, 'last_update':None}

class NiblitSensors:
    def __init__(self):
        print('[Niblit Sensors] Initializing sensors...')
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def read_sensors(self):
        lat = -33.93 + random.uniform(-0.01, 0.01)
        lon = 18.42 + random.uniform(-0.01, 0.01)
        SENSOR_STATUS['gps'] = {'lat': round(lat,4), 'lon': round(lon,4)}
        SENSOR_STATUS['camera'] = False
        SENSOR_STATUS['microphone'] = False
        SENSOR_STATUS['last_update'] = time.strftime('%Y-%m-%d %H:%M:%S')
        print('[Niblit Sensors]', SENSOR_STATUS)

    def _monitor_loop(self):
        while True:
            try:
                self.read_sensors()
            except Exception as e:
                print('[Niblit Sensors] Error:', e)
            time.sleep(30)

    def start_monitor(self):
        if not self._thread.is_alive():
            self._thread.start()