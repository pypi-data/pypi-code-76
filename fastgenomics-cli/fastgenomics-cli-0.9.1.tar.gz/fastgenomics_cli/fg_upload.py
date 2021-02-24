import logging
import argparse
import sys
from getpass import getpass
from update_checker import update_check
from fastgenomics import FASTGenomicsClient, FASTGenomicsDatasetClient
from . import __version__

log = logging.getLogger(__name__)


def main():
    print(f"FASTGenomics upload tool version {__version__}")
    update_check('fastgenomics_upload', __version__)

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("file", nargs="+", type=str, help="the file(s) to be uploaded")
    parser.add_argument('-v', '--verbose', action='store_true', help="more verbose output")
    parser.add_argument('-d', '--dataset', help="add file to existing dataset with this id", type=str, default=None)
    parser.add_argument('-u', '--user', type=str, default=None, help="your username (or email address)")
    parser.add_argument('-p', '--password', type=str, default=None, help="your password")
    parser.add_argument('-t', '--title', type=str, default=None, help="the title of the new dataset")
    parser.add_argument('-m', '--metadata', help='upload files as metadata instead of expression data', action='store_true')
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        format="%(asctime)s [%(name)-19.19s] [%(levelname)-3.3s] %(message)s"
        # level=log_level
    )
    log.setLevel(log_level)
    FASTGenomicsClient.set_log_level(log_level)

    if args.dataset is not None and args.title is not None:
        log.error("When adding files to an existing dataset, you can't specify the dataset's title")
        sys.exit(1)

    client = FASTGenomicsDatasetClient()

    if args.user is not None or args.password is not None or not client.is_logged_in():
        if args.user is None:
            args.user = input('Please enter your username: ')
        if args.password is None:
            args.password = getpass('Please enter your password: ')
        try:
            client.login(args.user, args.password, login_method='password')
        except:
            log.error('Login failed. Did you provide the correct username and password?')
            sys.exit(1)

    if args.dataset is None:
        if args.title is None:
            args.title = input(f"Please enter the title of the dataset you want to create: [default: {args.file[0]}]")
        if args.title is None or args.title == '':
            args.title = args.file[0]
        log.info(f"creating dataset with title '{args.title}'")
        try:
            r = client.create_dataset(args.title)
            args.dataset = r.json()['id']
        except Exception as e:
            log.error(f"Failed to create dataset: {e}")
            sys.exit(1)

    for file in args.file:
        log.info(f"uploading '{file}'")
        try:
            client.add_file_to_dataset(args.dataset, file, 'metadata' if args.metadata else 'expressiondata', show_progress_bar=True)
        except Exception as e:
            log.error(f"Failed to upload '{file}': {e}")


if __name__ == '__main__':
    main()
