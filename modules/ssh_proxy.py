# modules/ssh_proxy.py
import os, subprocess, logging
log = logging.getLogger("ssh-proxy")
KEY_DIR = "data/keys"
os.makedirs(KEY_DIR, exist_ok=True)

def store_ssh_key(name, key_text):
    path = os.path.join(KEY_DIR, f"{name}.pub")
    with open(path,"w") as f:
        f.write(key_text)
    return path

def ensure_ssh_tunnel(remote_host, local_port, remote_port, keyfile=None):
    # This is a helper to call ssh -N -L ...; on Android this may not be available.
    cmd = ["ssh", "-o", "ExitOnForwardFailure=yes", "-L", f"{local_port}:127.0.0.1:{remote_port}", remote_host, "-N"]
    if keyfile:
        cmd = ["ssh", "-i", keyfile] + cmd[1:]
    log = subprocess.Popen(cmd)
    return log