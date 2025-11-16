# niblit_core.py - central orchestrator and state manager
import threading, time
from datetime import datetime
import niblit_network, self_maintenance, niblit_sensors, niblit_voice
import collector, trainer, generator, membrane, healer, slsa_generator, niblit_memory

class niblitcore:
    def __init__(self):
        self.name = "Niblit"
        self.start_time = datetime.utcnow().isoformat() + "Z"
        # init modules
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

        # background heartbeat
        threading.Thread(target=self._background_loop, daemon=True).start()

    def _background_loop(self):
        while True:
            try:
                self.collector.flush_if_needed()
                self.trainer.step_if_needed()
            except Exception as e:
                print("[NiblitCore] background error:", e)
            time.sleep(5)

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
        return "Niblit: " + text