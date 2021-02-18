"""Module for using Hurricane Electric's API"""
import logging
import requests


class HurricaneElectric:  # pylint: disable=too-few-public-methods
    """HurricaneElectric
    ---
    Class that deals with records for HurricaneElectric
    """

    def __init__(self, CONFIG, version):
        self.Config = CONFIG["Hurricane Electric"]
        self.log = logging.getLogger("PDDNS")
        self.version = version

        self.log.info("Hurricane Electric selected")

    def main(self, ip: str, _):
        """send
        ---

        Arguments:
            ip {str} -- The IP address for the record to point to.
        """
        BASE_URL = "https://dyn.dns.he.net/nic/update"
        header = {"User-Agent": f"PDDNS v{self.version}"}
        data = {
            "hostname": self.Config["Name"],
            "password": self.Config["Password"],
            "myip": ip,
        }
        r = requests.post(BASE_URL, data=data, headers=header)
        self.log.debug(r.text)
        r.raise_for_status()
