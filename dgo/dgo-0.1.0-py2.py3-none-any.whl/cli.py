"""Console script for dgo."""
import sys
import click
import requests


@click.group()
def main(args=None):
    return 0


@main.command()
@click.argument('local_file_path', type=click.File('rb'))
def upload(local_file_path):
    """
    Temporary upload a file.
    Then can download it later.
    But not guarantee when to delete from the server.
    So do not upload your importance file here.
    """
    ret = requests.post('http://tmp.daimon.cc:10080/upload', files={
        'file': local_file_path
    })
    click.secho('wget %s' % (ret.text.split(':', 1)[1].strip()), fg='cyan')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
