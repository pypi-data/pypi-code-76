"""Module for using provide api"""
import logging
import requests

import dns.resolver


class Provider:  # pylint: disable=too-few-public-methods
    """Reuseable code between different providers.
    ---

    This class implements methods that can be used from different providers.
    """

    def __init__(self, CONFIG, version):
        self.Config = CONFIG
        self.log = logging.getLogger("PDDNS")
        self.version = version

    def is_ip_uptodate(self, ip: str, ipv6: str):
        """check if IP address is up-to-date

        Some provider will block the domain, if they detect to many update requests
        without changes.

        A nameserver of the provider should be set because it will be updated fast. This
        method compare the ip address of the nameserver with the actual ip address.

        Args:
            ip (str): actual IPv4 address
            ipv6 (str): actual IPv6 address

        Returns:
            bool: True, if IP address is uptodate
        """
        resolver = dns.resolver.Resolver()
        if "Nameservers" in self.Config.keys():
            nameservers = self.Config["Nameservers"].split(",")

            for ns in nameservers:
                for record in ["A", "AAAA"]:
                    try:
                        nsips = dns.resolver.resolve(ns, record)
                        for nsip in nsips:
                            resolver.nameservers.insert(0, nsip.to_text())
                    except dns.resolver.NXDOMAIN:
                        self.log.warning("nameserver %s does not exist", ns)
                    except dns.resolver.NoAnswer:
                        pass

        name = self.Config["Name"]
        if ip:
            try:
                answers = resolver.resolve(name, "A")
                if not str(answers[0]) == ip:
                    return False
            except dns.resolver.NoAnswer:
                return False
        if ipv6:
            try:
                answers = resolver.resolve(name, "AAAA")
                if not str(answers[0]) == ipv6:
                    return False
            except dns.resolver.NoAnswer:
                return False
        self.log.debug("IP has not changed")
        return True

    def update_nic(self, url: str, ip: str):
        """Update ip address with a get request to nic/update:

        https://<login-data>@<url>/nic/update?hostname=<Name>&myip=<ip>

        Args:
            url (str): url of the provider
            ip (str): ip address
        """
        login_data = f"{self.Config['User']}:{self.Config['Password']}"
        BASE_URL = f"https://{login_data}@{url}/nic/update"
        header = {"User-Agent": f"PDDNS v{self.version}"}
        data = {"hostname": self.Config["Name"], "myip": ip}
        r = requests.get(BASE_URL, params=data, headers=header)
        self.log.debug(r.text)
        r.raise_for_status()
