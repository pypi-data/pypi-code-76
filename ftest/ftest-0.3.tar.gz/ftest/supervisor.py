import json
import socket
import sys
import time
from threading import Thread

from fcp import CANMessage, Fcp, FcpCom, Spec
from result import Ok, Err

from .vio import adc_pack


class Proxy:
    def __init__(self, socket, addrs):
        self.socket = socket
        self.socket.settimeout(1)
        self.addrs = addrs

        self.cmds = {}

    def recv(self) -> CANMessage:
        try:
            msg, _ = self.socket.recvfrom(1024)
            return Ok(CANMessage.decode_json(msg))
        except Exception as e:
            return Err("Timeout")

    def send(self, msg: CANMessage):
        for addr in self.addrs:
            self.socket.sendto(msg.encode_json(), addr)


class Supervisor:
    def contact_vsniffer(self):
        hello_msg = bytes(
            json.dumps({"sid": 1, "dlc": 1, "data": [0, 1, 2, 3], "timestamp": 0}),
            "ascii",
        )

        for addr in self.addrs:
            # print_console("Contacting vsniffer ---> Port: " + str(addr[0]), False, cfg)
            self.vsniffer.sendto(hello_msg, addr)

    def contact_middleman(self):
        self.middle.sendto(adc_pack("ola", 0), ("127.0.0.1", 9999))

    def __init__(self, cfg):
        self.signals = {}
        self.console_mode = cfg["repl"]

        self.fcp = Fcp(cfg["root"] + "/lib/can-ids-spec/fst10e.json")

        self.addrs = [(cfg["vsniffer_ip"], port) for port in cfg["vsniffer_ports"]]
        self.vsniffer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.contact_vsniffer()

        self.fcpcom = FcpCom(self.fcp, Proxy(self.vsniffer, self.addrs))
        self.fcpcom.start()

        self.middle = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.contact_middleman()

        self.thread = Thread(target=self.run)
        self.thread.start()

    def register_signal(self, signals):
        for name, value in signals.items():
            self.signals[name] = value

    def get_signal(self, sig_name):
        # Check for value changes
        previous_value = None
        matches = 0
        null_matches = 0
        while matches < 5:
            current_value_err = 100
            while current_value_err > 1e-3:
                if self.signals[sig_name] == 0:
                    null_matches += 1
                    if null_matches > 100:
                        break
                    continue
                null_matches = 0
                if previous_value is not None:
                    current_value_err = abs(
                        round(previous_value - self.signals[sig_name], 2)
                    )
                previous_value = self.signals[sig_name]
                if current_value_err > 1e-3:
                    matches = 0
            matches += 1
            time.sleep(0.02)
        return self.signals[sig_name]

    def stop(self):
        self.terminate = True
        self.thread.join()
        self.fcpcom.stop()

    def run(self):
        self.terminate = False
        while not self.terminate:
            try:
                msg_name, signals = self.fcpcom.q.get(timeout=1)
            except Exception as e:
                continue
            self.register_signal(signals)
