# self_maintenance.py - health monitor with Android-safe fallbacks
import threading, time
try:
    import psutil
    PSUTIL_AVAILABLE = True
except Exception:
    psutil = None
    PSUTIL_AVAILABLE = False

class SelfMaintenance:
    def __init__(self):
        print('[SelfMaintenance] Module initialized.')
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def safe_cpu_percent(self):
        try:
            if PSUTIL_AVAILABLE:
                return psutil.cpu_percent(interval=0.5)
        except Exception:
            pass
        return -1

    def safe_mem_percent(self):
        try:
            if PSUTIL_AVAILABLE:
                return psutil.virtual_memory().percent
        except Exception:
            pass
        return -1

    def diagnose(self):
        cpu = self.safe_cpu_percent()
        mem = self.safe_mem_percent()
        print(f'[SelfMaintenance] CPU: {cpu}% | RAM: {mem}%')

    def _monitor_loop(self):
        while True:
            try:
                self.diagnose()
            except Exception as e:
                print('[SelfMaintenance] Error:', e)
            time.sleep(10)

    def start_monitor(self):
        if not self._thread.is_alive():
            self._thread.start()