'''


Cases:
 - user-created process
    - launch thread to monitor process health
    - if process goes down:
        - should a new one


'''
import time
import remoteobj
import subprocess



class SingleProcess:
    _monitor_interval = 1
    _thread = None
    def __init__(self, command, name):
        self.command = command
        self.name = name

    def spawn(self):
        if self._thread is not None:
            return
        self._thread = remoteobj.util.thread(self._monitor_thread)

    def join(self):
        if self._thread is None:
            return
        self._thread.join()
        self._thread = None

    _proc = None
    _mine = False
    def _monitor_thread(self):
        import psutil
        while True:
            if self._proc is None or not self._proc.is_alive():
                self._mine = False
                with lock:
                    self._proc = next((p for p in psutil.process_iter() if self.name in p.name()), None)
                    if self._proc is None:
                        self._proc = subprocess.Popen(
                            shlex.split(self.command),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
                        self._mine = True
                        self.stdout = self._proc.stdout
                        self.stderr = self._proc.stderr
            time.sleep(self._monitor_interval)
