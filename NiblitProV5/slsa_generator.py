# slsa_generator.py - simple SBOM-like generator
import os, json, time
def generate_sbom(output='sbom.json'):
    root = os.getcwd()
    artifacts = []
    for fn in os.listdir(root):
        if fn.endswith('.py'):
            artifacts.append({'file': fn, 'mtime': os.path.getmtime(fn)})
    sbom = {'generated': time.time(), 'artifacts': artifacts}
    with open(output, 'w') as f:
        json.dump(sbom, f, indent=2)
    print('[SLSaGen] SBOM written to', output)
    return output

def init():
    print('[SLSaGen] ready')