#!/usr/bin/env python3

import time

def bytes_to_human(size):
    """
    Convert Bytes to more readable units
    """
    units = [ 'B', 'kB', 'MB', 'GB', 'TB' ]
    unit_idx = 0    # Start with Bytes
    while unit_idx < len(units)-1:
        if size < 2048:
            break
        size /= 1024.0
        unit_idx += 1
    return size, units[unit_idx]

def seconds_to_human(seconds, decimal=3):
    """
    Convert seconds to HH:MM:SS[.SSS]

    If decimal==0 only full seconds are used.
    """
    secs = int(seconds)
    fraction = seconds - secs

    mins = int(secs / 60)
    secs = secs % 60

    hours = int(mins / 60)
    mins = mins % 60

    ret = f"{hours:02d}:{mins:02d}:{secs:02d}"
    if decimal:
        fraction = int(fraction * (10**decimal))
        ret += f".{fraction:0{decimal}d}"

    return ret

class InterfaceStats:
    def __init__(self, interface_name, avg_secs=10, refresh=0.5):
        self._interface_name = interface_name
        self.avg_secs = avg_secs
        self.refresh = refresh

        self._open_files = {}
        self.stats = { 'ts': 0, 'rx': 0, 'tx': 0 }

    def _read_sysfile(self, filename):
        if not filename in self._open_files:
            self._open_files[filename] = open(f"/sys/class/net/{self._interface_name}/statistics/{filename}", "rt")
        else:
            self._open_files[filename].seek(0)
        return int(self._open_files[filename].readline().strip())

    def get_stats(self):
        """
        Return dict with interface statistics.
        """
        return {
            'ts': time.time(),
            'rx': self._read_sysfile('rx_bytes'),
            'tx': self._read_sysfile('tx_bytes'),
        }

    def display_stats(self):
        def _erase_line():
            print('\r\x1B[K', end="")   # Erase line

        stat_history = [self.stats]
        stat_history_len = int(self.avg_secs / self.refresh)
        start_ts = time.time()

        while True:
            time.sleep(self.refresh)

            # Take another 'stat' snapshot
            stat_history.insert(1, self.get_stats())

            # Calculate sliding window average
            if stat_history[1]['ts'] > stat_history[-1]['ts']:
                tx_avg = (stat_history[1]['tx'] - stat_history[-1]['tx'])/(stat_history[1]['ts'] - stat_history[-1]['ts'])
                rx_avg = (stat_history[1]['rx'] - stat_history[-1]['rx'])/(stat_history[1]['ts'] - stat_history[-1]['ts'])
            else:
                tx_avg = rx_avg = 0.0

            # Trim the oldest points
            del(stat_history[stat_history_len+1:])

            uptime = seconds_to_human(time.time()-start_ts, decimal=0)
            tx_t_h, tx_t_u = bytes_to_human(stat_history[1]['tx'])
            rx_t_h, rx_t_u = bytes_to_human(stat_history[1]['rx'])
            tx_a_h, tx_a_u = bytes_to_human(tx_avg)
            rx_a_h, rx_a_u = bytes_to_human(rx_avg)

            _erase_line()
            print(f"{uptime} | In: {rx_t_h:6.1f}{rx_t_u:>2s} @ {rx_a_h:6.1f}{rx_a_u:>2s}/s | Out: {tx_t_h:6.1f}{tx_t_u:>2s} @ {tx_a_h:6.1f}{tx_a_u:>2s}/s", end="", flush=True)

if __name__ == "__main__":
    ifc = InterfaceStats('enp0s31f6')
    print(ifc.get_stats())
    time.sleep(1)
    print(ifc.get_stats())
    ifc.display_stats()
