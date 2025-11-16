# niblit_memory.py - simple persistent memory manager
import json, os
class MemoryManager:
    def __init__(self, path='data/memory.json'):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        try:
            with open(path,'r') as f:
                self.data = json.load(f)
        except:
            self.data = {}

    def set(self, k, v):
        self.data[k] = v
        with open(self.path,'w') as f:
            json.dump(self.data, f, indent=2)

    def get(self, k, default=None):
        return self.data.get(k, default)