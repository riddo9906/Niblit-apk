# main_refactor.py
import os
os.environ['KIVY_METRICS_DENSITY'] = '1'
os.environ['KIVY_WINDOW'] = 'sdl2'

from niblit_core import niblitcore
from niblit_dashboard import launch_dashboard

def run_system():
    print("[Niblit] Booting system...")
    core = niblitcore()

    print("[Niblit] Launching dashboard (main thread)...")
    # KivyMD must run on main thread
    launch_dashboard(core)

if __name__ == "__main__":
    run_system()