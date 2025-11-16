import subprocess

class ConsoleModule:
    def run_command(self, cmd):
        try:
            return subprocess.check_output(cmd, shell=True, text=True)
        except Exception as e:
            return f"Error: {e}"