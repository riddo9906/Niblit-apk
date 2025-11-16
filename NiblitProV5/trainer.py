# trainer.py - trainer stub
import time, json, os

class Trainer:
    def __init__(self, collector, path='data/training_queue.json'):
        self.collector = collector
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def step_if_needed(self):
        pending = self.collector.get_pending()
        if pending:
            artifact = {'ts': time.time(), 'count': len(pending)}
            with open(self.path, 'a') as f:
                f.write(json.dumps(artifact) + '\\n')
            print('[Trainer] Produced training artifact:', artifact)