import click
import urllib3
import threading
import os

from .constants import *
from requests.exceptions import HTTPError
from search_python_client.search import DrsClient


def is_drs_url(url):
    return url[:3] == 'drs'


def download_file(drs_url, url, output_dir):
    drs_client = DrsClient(drs_url)
    http = urllib3.PoolManager()
    chunk_size = 1024
    download_url = url

    object_id = url.split('/')[-1]
    if is_drs_url(url):
        # parse the drs url to the resource url
        try:
            object_info = drs_client.get_object_info(object_id)
        except HTTPError as e:
            click.echo(e)
            if '404' in e.response:
                click.secho("There was an error getting object into from the DRS Client", fg='red')
            return
        except:
            return

        if "access_methods" in object_info.keys():
            for access_method in object_info["access_methods"][0]:
                if access_method['type'] == 'access_id':
                    click.echo("found access_id @ access_method level")
                # if we have an https, use that
                if access_method['type'] == 'https':
                    if 'access_id' in access_method['access_url'].keys():
                        click.echo("found access_id @ access_url level")
                    download_url = access_method['access_url']['url']
                    break
        else:
            return  # next page token, just return

    try:
        download_stream = http.request('GET', download_url, preload_content=False)
    except:
        click.secho("There was an error downloading " + download_url, fg='red')
        return

    with open(f"{output_dir}/{download_url.split('/')[-1]}", 'wb+') as dest:
        while True:
            data = download_stream.read(chunk_size)
            if not data:
                break
            dest.write(data)


def download_files(drs_url, urls, output_dir=downloads_directory):
    download_threads = []

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in urls:
        download = threading.Thread(target=download_file(drs_url, url, output_dir), name=url)
        download.daemon = True
        download_threads.append(download)
        download.start()

    for thread in download_threads:
        thread.join()

    click.secho("Download Complete into " + output_dir, fg='green')
