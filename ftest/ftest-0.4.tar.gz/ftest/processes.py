import os
import signal
import subprocess
import sys
import time
from pathlib import Path

class ProcessMonitor():
    def __init__(self, config):
        self.config = config
        self.launch_table = {}

    def launch(self):
        middleman_dir = Path(self.config["root"]) / self.config["middleman"]
        middle_exe = middleman_dir / "middleman.py"
        middle_cfg = middleman_dir / "config.toml"
        vsniffer_dir = Path(self.config["root"]) / self.config["vsniffer"]
        vsniffer_exe = vsniffer_dir / "vsniffer.py"
        vsniffer_cfg = vsniffer_dir / "config.toml"


        self.middle = subprocess.Popen(
            f"python3 {middle_exe} {middle_cfg} >> middleman.log 2>&1",
            shell=True,
            preexec_fn=os.setsid,
        )
        self.vsniffer = subprocess.Popen(
            f"python3 {vsniffer_exe} {vsniffer_cfg} >> vsniffer.log 2>&1",
            shell=True,
            preexec_fn=os.setsid,
        )

        time.sleep(1)


        # kill middleman and vsniffer if they fail to launch and terminate the program
        if self.middle.poll() is not None or self.vsniffer.poll() is not None:
            print("Error failed to launch middleman and vsniffer")
            self.kill()
            sys.exit(1)


    def kill(self):
        for value in self.launch_table.values():
            os.killpg(os.getpgid(value.pid), signal.SIGTERM)

        try:
            os.killpg(os.getpgid(self.middle.pid), signal.SIGTERM)
        except Exception as e:
            pass
        try:
            os.killpg(os.getpgid(self.vsniffer.pid), signal.SIGTERM)
        except Exception as e:
            pass

