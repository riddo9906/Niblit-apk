#niblit_core_refactor.py
import threading, time
from datetime import datetime

# Import existing modules
import niblit_network, self_maintenance, niblit_sensors, niblit_voice
import collector, trainer, generator, membrane, healer, slsa_generator, niblit_memory

class niblitcore:
    def __init__(self):
        self.name = "Niblit"
        self.start_time = datetime.utcnow().isoformat() + "Z"

        # Core service modules
        self.network = niblit_network.network
        self.self_maintenance = self_maintenance.SelfMaintenance()
        self.sensors = niblit_sensors.NiblitSensors()
        self.voice = niblit_voice.NiblitVoice()
        self.collector = collector.Collector()
        self.trainer = trainer.Trainer(self.collector)
        self.generator = generator.Generator()
        self.membrane = membrane.Membrane()
        self.healer = healer
        self.slsa = slsa_generator
        self.memory = niblit_memory.MemoryManager()

        # -----------------------
        # New ecosystem service hooks
        # -----------------------
        self.production_services = []   # factories, workshops
        self.farm_services = []         # farm/energy/food modules
        self.replication_services = []  # self-replicating business builder units
        self.sales_services = []        # customer/sales interface
        self.health_services = []       # human/system monitoring

        # Background task manager
        self._tasks = []
        self._start_background_loop()

    def _start_background_loop(self):
        t = threading.Thread(target=self._background_loop, daemon=True)
        t.start()

    def _background_loop(self):
        while True:
            try:
                # Collect & train
                self.collector.flush_if_needed()
                self.trainer.step_if_needed()

                # Update sensors & health modules
                self.sensors.read_sensors()
                self.self_maintenance.diagnose()

                # TODO: Integrate production/farm/sales/replication logic
            except Exception as e:
                print("[NiblitCore] background error:", e)
            time.sleep(5)

    # Example respond method with ecosystem hook
    def respond(self, text):
        text = text.lower().strip()
        if "time" in text:
            return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        if "weather" in text:
            return str(self.network.get_weather())
        if "news" in text:
            return str(self.network.get_news())
        if text.startswith("remember"):
            try:
                _, rest = text.split(" ",1)
                k,v = rest.split(":",1)
                self.memory.set(k.strip(), v.strip())
                return f"Remembered {k.strip()}."
            except:
                return "Use: remember key: value"
        # Future integration: send commands to production/farm/sales/replication modules
        return "Niblit: " + text

    # Core shutdown
    def shutdown(self):
        print("[NiblitCore] shutting down...")
        try:
            self.network.shutdown()
        except:
            pass
        print("[NiblitCore] shutdown complete.")