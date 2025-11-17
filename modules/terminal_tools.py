# modules/terminal_tools.py
import subprocess, shlex, os

def run(cmd, timeout=10):
    try:
        proc = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return proc.stdout.decode('utf-8') + proc.stderr.decode('utf-8')
    except Exception as e:
        return str(e)

def read_file(path):
    try:
        with open(path,'r',encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return str(e)

def write_file(path, content):
    try:
        d = os.path.dirname(path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
        with open(path,'w',encoding='utf-8') as f:
            f.write(content)
        return "OK"
    except Exception as e:
        return str(e)