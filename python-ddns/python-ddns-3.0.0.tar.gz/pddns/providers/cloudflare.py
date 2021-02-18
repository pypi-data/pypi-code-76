"""Module for using Cloudflare's API"""
import logging
from typing import Union, Any
import requests


class Cloudflare:
    """Cloudflare
    ---

    Class that deals with records for Cloudflare.
    """

    def __init__(self, CONFIG, version):
        self.Config = CONFIG["Cloudflare"]
        self.log = logging.getLogger("PDDNS")
        self.version = version

        self.log.info("Cloudflare selected")

    def main(self, ip: str, _) -> None:
        """main
        ---

        Arguments:
        ---
            ip {str} -- The IP address that the new record will have.
        """
        check = self.check_record()
        if check:
            self.update_record(ip, check)
        else:
            self.add_record(ip)

    def check_record(self) -> Union[str, bool]:
        """check_record
        ---

        Checks if an existing record already exists

        Returns:
            Union[str, bool] -- Returns either the record if it
                                exists or False if it does not exist.
        """
        record = {"type": "A", "name": self.Config["Name"]}
        output = self.send(record, "get")
        self.log.debug(output)
        if not output["success"]:
            raise Exception(
                "The check failed with error code {}".format(
                    output["errors"][0]["code"]
                )
            )
        if output["result"]:
            return output["result"][0]["id"]
        return False

    def add_record(self, ip: str) -> None:
        """add_record
        ---

        Creates a new A record.

        Arguments:
            ip {str} -- [description]
        """
        record = {
            "type": "A",
            "name": self.Config["Name"],
            "content": ip,
            "proxied": self.Config.getboolean("Proxied"),
        }
        output = self.send(record, "post")
        if not output["success"]:
            try:
                error_code = output["errors"][0]["error_chain"][0]["code"]
                self.log.error(error_code)
            except KeyError:
                error_code = output["errors"][0]["code"]
                self.log.error(error_code)
            else:
                self.log.error("There was an error\n")
                self.log.error(output["errors"])
                self.log.error(error_code)
        if output["success"]:
            self.log.info("The record was created successfully")

    def update_record(self, ip: str, record_id: str) -> None:
        """update_record
        ---

        Updates an existing record.

        Arguments:
            ip {str} -- The IP Address to be updated.
            record_id {str} -- The record_id of the record to update.
        """
        record = {"type": "A", "name": self.Config["Name"], "content": ip}
        output = self.send(record, "put", record_id)
        if not output["success"]:
            self.log.error("There was an error:")
            self.log.error(output)
        else:
            self.log.info("Record updated successfully")

    # pylint: disable=inconsistent-return-statements
    def send(self, content: dict, which: str, extra: str = None) -> Union[Any, bool]:
        """send
        ---

        Function that sends the information

        Arguments:
            content {dict} -- [description]
            which {str} -- [description]

        Keyword Arguments:
            extra {str} -- The currect record_id if there is one
                           (default: {None})

        Returns:
            Union[Any, bool] -- [description]
        """
        headers = {
            "Authorization": f"Bearer {self.Config['API_Token']}",
            "X-Auth-Email": self.Config["Email"],
            "Content-Type": "application/json",
            "User-Agent": f"PDDNS v{self.version}",
        }
        api_url = (
            "https://api.cloudflare.com/client/v4/zones/"
            + self.Config["Zone"]
            + "/dns_records"
        )
        # GET Request
        if which == "get":
            r = requests.get(api_url, json=content, headers=headers).json()
            self.log.debug(r)
        # POST Request
        elif which == "post":
            r = requests.post(api_url, json=content, headers=headers).json()
            self.log.debug(r)
        # PUT Request
        elif which == "put":
            api_url = api_url + "/" + extra
            r = requests.put(api_url, json=content, headers=headers).json()
            self.log.debug(r)
        return r
