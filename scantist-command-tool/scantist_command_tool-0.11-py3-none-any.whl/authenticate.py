import getopt
import logging
import sys

from command_tool.utils.login import login, registration
from command_tool.utils.utils import error_exit, set_config

FORMAT = "%(asctime)s|%(levelname)s|%(message)s"
logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO, format=FORMAT)

HELP_CONTENT = """
Login and save credentials
\t> scantist_auth -b $baseurl -e $email/-u $username -p $password
Set up base url and apikey:
\t> scantist_auth -b $base_url -a apikey
Register a new user and set up everything
\t> scantist_auth -b $base_url -e $email -u username -p $password -c
"""


def main():
    argv = sys.argv[1:]
    opts = []
    args = []
    email = ""
    password = ""
    base_url = ""
    api_key = ""
    username = ""
    mode_create = False
    try:
        opts, args = getopt.getopt(
            argv,
            "hce:p:b:a:u:",
            [
                "email=",
                "password=",
                "base_url=",
                "api_key=",
                "username=",
            ],
        )
    except Exception as e:
        error_exit(e)

    if len(args) == 0 and len(opts) == 0:
        logger.info(HELP_CONTENT)
        exit(0)

    for opt, arg in opts:
        if opt == "-h":
            logger.info(HELP_CONTENT)
            sys.exit()
        elif opt in ("-c", "--create"):
            mode_create = True
        elif opt in ("-e", "--email"):
            email = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-b", "--base_url"):
            base_url = arg
        elif opt in ("-a", "--api_key"):
            api_key = arg
        elif opt in ("-u", "--username"):
            username = arg

    if base_url:
        set_config("SCANTIST", "base_url", base_url)
    else:
        error_exit("Missing required parameter -b/--base_url.")

    if api_key:
        set_config("SCANTIST", "api_key", api_key)
        exit(0)

    if not username and not email:
        error_exit("Required username/email missing.")

    if not password:
        error_exit("Required password missing.")

    if mode_create:
        r = registration(username if username else email, email, password, base_url)
        logger.info(f"[Registration]==>{r}")
    else:
        r = login(email, password, "", base_url, username=username)
        logger.info(f"[LOGIN]==>{r}")


#
# if __name__ == "__main__":
#     main(sys.argv[1:])
