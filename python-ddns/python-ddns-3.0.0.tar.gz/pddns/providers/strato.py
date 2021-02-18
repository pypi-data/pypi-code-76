"""Module for using Strato's API"""
from .common import Provider


class Strato(Provider):  # pylint: disable=too-few-public-methods
    """Strato
    ---

    Class that deals with records for Strato.
    """

    def __init__(self, CONFIG, version):
        super().__init__(CONFIG["Strato"], version)
        self.log.info("Strato selected")

    def main(self, ip: str, ipv6: str) -> None:
        """main
        ---
        Strato supports IPv4 and IPv6. Both addresses will be connect to a string and
        separated with a comma. (like 1.2.3.4,2001:0db8:85a3:08d3:1319:8a2e:0370:7344)

        Arguments:
        ---
            ip {str} -- The IP address that the new record will have.
            ipv6 {str} -- The IPv6 address that the new record will have.
        """
        if ip and ipv6:
            new_ips = ip + "," + ipv6
        elif ip:
            new_ips = ip
        elif ipv6:
            new_ips = ipv6
        else:
            raise ValueError("IPv4 and IPv6 address is empty")
        if self.is_ip_uptodate(ip, ipv6):
            return
        self.update_nic("dyndns.strato.com", new_ips)
