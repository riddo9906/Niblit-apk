# generator.py - creative generator and seed manager
import time, random

class Generator:
    def __init__(self):
        self.seed = int(time.time())

    def create_seed(self):
        self.seed = (self.seed * 1103515245 + 12345) & 0x7fffffff
        return self.seed

    def synthetic_thought(self):
        seeds = ['curious','observe','plan','recall','imagine']
        return random.choice(seeds) + '-' + str(self.create_seed())