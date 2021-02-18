"""Module for using Afraid's API"""
from .common import Provider


class Afraid(Provider):  # pylint: disable=too-few-public-methods
    """Afraid
    ---

    Class that deals with records for Afraid.
    """

    def __init__(self, CONFIG, version):
        super().__init__(CONFIG["Afraid"], version)
        self.log.info("Afraid selected")

    def main(self, ip: str, ipv6: str) -> None:
        """main
        ---
        Afraid.org supports either IPv4 or IPv6. An IPv6 address will be preferred.

        Arguments:
        ---
            ip {str} -- The IP address that the new record will have.
            ipv6 {str} -- The IPv6 address that the new record will have.
        """
        if ipv6:
            new_ip = ipv6
            if self.is_ip_uptodate(None, ipv6):
                return
        elif ip:
            new_ip = ip
            if self.is_ip_uptodate(ip, None):
                return
        else:
            raise ValueError("IPv4 and IPv6 address is empty")
        self.update_nic("freedns.afraid.org", new_ip)
