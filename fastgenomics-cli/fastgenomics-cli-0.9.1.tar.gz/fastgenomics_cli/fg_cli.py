#!/usr/bin/env python3

"""
FASTGenomics Commandline Interface (CLI)
"""

__copyright__ = "Copyright, Comma Soft AG"
__version__ = "0.2.0"
__maintainer__ = "Ralf Karle"
__email__ = "ralf.karle@comma-soft.com"

import argparse
import datetime
import json
import logging
import sys
from os import path

logger = logging.getLogger(__name__)
log_level = logging.WARN

from fastgenomics import FASTGenomicsClient, FASTGenomicsLargeFileStorageClient, FASTGenomicsDatasetClient, run_zip, ToolConfiguration

def _add_parser(parser, name: str, helptext: str, description: str = "", epilog: str = "", action: str = ""):
    if description == "":
        description = helptext

    if action == "":
        action = name

    if epilog != "":
        new_parser = parser.add_parser(
            name, help=helptext, description=description)
    else:
        new_parser = parser.add_parser(
            name, help=helptext, description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)

    new_parser.set_defaults(action=action)

    new_parser.add_argument("-v", "--verbose",
                            help="Activate verbose output", action='count', default=0)

    return new_parser


def parse_args():
    desc = R"""
 ______       _____ _______ _____                            _
|  ____/\    / ____|__   __/ ____|                          (_)
| |__ /  \  | (___    | | | |  __  ___ _ __   ___  _ __ ___  _  ___ ___
|  __/ /\ \  \___ \   | | | | |_ |/ _ \ '_ \ / _ \| '_ ` _ \| |/ __/ __|
| | / ____ \ ____) |  | | | |__| |  __/ | | | (_) | | | | | | | (__\__ \
|_|/_/    \_\_____/   |_|  \_____|\___|_| |_|\___/|_| |_| |_|_|\___|___/

Welcome to FASTGenomics CLI!

Here are the base commands:
"""
    parser = argparse.ArgumentParser(
        description=desc, formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers(
        title="FASTGenomics CLI", help="Actions for FASTGenomics")

    login_parser = _add_parser(
        subparsers, "login", helptext="Log in to FASTGenomics.")
    login_parser.add_argument(
        "-u", "--user", help="the FASTGenomics user", required=True)
    login_parser.add_argument(
        "-p", "--passphrase", help="the passphrase of FASTGenomics user", required=True)
    login_parser.add_argument(
        "-m", "--login_method", help="the login method 'pat' (personal access token) or 'password'. Default: pat",
        choices=["pat", "password"], default="pat")

    login_parser.add_argument(
        "--url", help="the url of the FASTGenomics plattform. Default: https://beta.fastgenomics.org",
        default="https://beta.fastgenomics.org")

    logout_parser = _add_parser(
        subparsers, "logout", helptext="Log out to remove access to FASTGenomics.")

    aws_parser = _add_parser(
        subparsers, "configure-aws", helptext="Configure AWS for FASTGenomics")

    epilog = """
output:

{
    "fg.py": "0.1"
}
"""
    version_parser = _add_parser(subparsers, "version", helptext="Show the version of FASTGenomics CLI.",
                                 description="Show the version of the cli client", epilog=epilog)

    lfs_parser = _add_parser(subparsers, "lfs", helptext="Manage Large File Storage (lfs)",
                             description="Group: fg lfs  - Manage FASTGenomics Large File Storage (lfs)")

    lfs_subparsers = lfs_parser.add_subparsers()

    lfs_create_parser = _add_parser(
        lfs_subparsers, "create", action="lfs-create", helptext="Create and upload a large file storage")

    lfs_create_parser.add_argument(
        "files_or_directory", nargs="+", type=str, help="file names or directory to be compressed")

    lfs_create_parser.add_argument("-z", "--zip-filename",
                                   help="name of the zip file", type=str, nargs="?")

    lfs_create_parser.add_argument("-P", "--zip-password",
                                   help="password for the zip file. if omitted a password will be generated.", type=str,
                                   nargs="?", required=False)

    lfs_create_parser.add_argument("-r", "--recipient-email",
                                   help="the email address used in FASTGenomics of the recipient", type=str,
                                   required=True)

    lfs_create_parser.add_argument("-T",
                                   "--title", help="the title of the FASTGenomics dataset containing the uploaded data",
                                   type=str, nargs='?', default="")

    lfs_create_parser.add_argument("--provider", help="the provider to be used 'azure' or 'aws'. Default: azure)",
                                   type=str, default='azure', nargs='?', choices=["azure", "aws"])

    lfs_create_parser.add_argument(
        "--skip-compression", help="Skip the compression", action='store_true')

    lfs_get_url_parser = _add_parser(
        lfs_subparsers, "get-url", helptext="Get a download url", action="lfs-get-downloadurl")
    lfs_get_url_parser.add_argument(
        "id", type=str, help="the id of the storage")
    lfs_get_url_parser.add_argument(
        "access_token", type=str, help="the access token")

    # ###### datasets #####

    dataset_parser = subparsers.add_parser(
        "dataset", help="Manage datasets", description="Group: fg dataset  - Manage FASTGenomics datasets.")

    dataset_subparsers = dataset_parser.add_subparsers()

    dataset_upload_parser = _add_parser(
        dataset_subparsers, "upload-file", action="dataset-upload", helptext="upload files to FASTGenomics dataset")
    dataset_upload_parser.add_argument(
        "files", nargs="+", type=str, help="file names of the files to be uploaded")
    dataset_upload_parser.add_argument(
        "-id", help="the id of the dataset", type=str, required=True)

    dataset_upload_parser.add_argument("-t",
                                       "--type",
                                       help="the type of the file 'expressionData' or 'metaData': Default: expressionData",
                                       type=str, default='expressiondata', nargs='?',
                                       choices=["expressiondata", "metadata"])

    dataset_delete_parser = _add_parser(
        dataset_subparsers, "delete", action="dataset-delete", helptext="delete a FASTGenomics dataset")
    dataset_delete_parser.add_argument(
        "-id", help="the id of the dataset", type=str, required=True)

    args = parser.parse_args()
    return args


def output(data: dict):
    """ output """
    j = json.dumps(data, indent=4)
    print(j)


def run():
    """ run """
    try:
        args = parse_args()

        level = logging.WARN
        if args.verbose == 0:
            pass
        elif args.verbose == 1:
            level = logging.INFO
        else:
            level = logging.DEBUG

        FASTGenomicsClient.set_log_level(level)

        if args.action == "lfs-create":
            title = args.title
            if title == "":
                title = "upload " + datetime.date.today().strftime("%d.%m.%Y %H:%M")

            recipient_email = args.recipient_email.lower()  # normalize it

            lfs = FASTGenomicsLargeFileStorageClient()

            zip_password = args.zip_password
            if args.skip_compression:
                assert len(
                    args.files_or_directory) == 1, "if compression is skipped the it has to be a single file"
                full_path = path.abspath(
                    path.expanduser(args.files_or_directory[0]))
                assert path.isfile(
                    full_path), "if compression is skipped the it has to be a single file"
                filename = full_path
            else:
                if zip_password is None or zip_password == "":
                    logging.debug("generating zip password")
                    zip_password = FASTGenomicsClient.generate_password()
                assert args.zip_filename is not None, "You have to provide a --zip-filename parameter."
                filename = run_zip(
                    args.files_or_directory, args.zip_filename, zip_password)

            result = lfs.upload_file_to_lfs(args.provider, filename, title,
                                            recipient_email, zip_password)
            output(result.__dict__)

        elif args.action == "lfs-get-downloadurl":
            lfs = FASTGenomicsLargeFileStorageClient()
            url = lfs.get_download_url(args.id, args.access_token)
            output({"download_url": url})

        elif args.action == "dataset-upload":
            results = []
            for file in args.files:
                logger.info(
                    f"uploading {args.type} file '{file}' to '{args.id}'")
                client = FASTGenomicsDatasetClient()
                result = client.add_file_to_dataset(args.id, file, args.type)
                results.append(result)
            output(results)

        elif args.action == "dataset-delete":
            client = FASTGenomicsDatasetClient()
            client.delete_dataset(args.id)

        elif args.action == "login":
            ToolConfiguration.ensure_config_json()  # ensure the config is created

            logger.info(f"login {args.user}")
            client = FASTGenomicsClient()
            client.login(args.user, args.passphrase,
                         args.login_method, args.url)
            output(client.fastgenomics_account.__dict__)

        elif args.action == "logout":
            logger.info("logout")
            client = FASTGenomicsClient()
            client.logout()

        elif args.action == "configure-aws":
            logger.info("configure aws")
            client = FASTGenomicsClient()
            print("Save this account information in a safe place.")
            print(
                "This account information is required by the FASTGenomics team to set up your AWS Large File Storage.")
            output(client.aws_configure_cloud())

        elif args.action == "version":
            logger.info("version")
            output(FASTGenomicsClient.version())
        else:
            raise RuntimeError(f"unknown action '{args.action}'")

    except Exception as err:
        logging.error(err)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    run()