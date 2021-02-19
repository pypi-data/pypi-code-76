#!/usr/bin/env python

import os, sys, json, textwrap, logging, fnmatch, mimetypes, datetime, time, base64, hashlib, concurrent.futures
from argparse import Namespace

import click, requests
from dateutil.parser import parse as dateutil_parse

from . import GSClient, GSUploadClient, GSBatchClient, logger
from .util import Timestamp, CRC32C, get_file_size, format_http_errors, batches
from .util.compat import makedirs, cpu_count
from .util.printing import page_output, tabulate, GREEN, BLUE, BOLD, format_number, get_progressbar
from .version import __version__


@click.group()
@click.version_option(version=__version__)
def cli():
    """
    Taxoniq: Taxon Information Query - fast, offline querying of NCBI Taxonomy and related data

    Run "taxoniq COMMAND --help" for command-specific usage and options.
    """
    logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("--taxon-id", help="")
@click.option("--accession-id", help="")
@click.option("--scientific-name", help="")
#@format_http_errors
def lineage(taxon_id=None, accession_id=None, scientific_name=None):
    """List all taxonomy nodes between this node and the root."""

cli.add_command(lineage)


@click.command()
@click.argument('paths', nargs=-1, required=True)
@click.option('--content-type', help="Set the content type to this value when uploading (guessed by default).")
@click.option('--content-encoding', help="Set the Content-Encoding header to this value (guessed by default).")
@click.option('--content-language', help="Set the Content-Language header to this value.")
@click.option('--content-disposition', help="Set the Content-Disposition header to this value.")
@click.option('--cache-control', help="Set the Cache-Control header to this value.")
@click.option('--metadata', multiple=True, metavar="KEY=VALUE", type=lambda x: x.split("=", 1),
              help="Set metadata on destination object(s) (can be specified multiple times).")
@format_http_errors
def cp(paths, **upload_metadata_kwargs):
    """
    Copy files to, from, or between buckets. Examples:

      gs cp * gs://my-bucket/my-prefix/

      gs cp gs://my-bucket/foo* .

      gs cp gs://my-bucket/foo gs://my-other-bucket/bar

    Use "-" to work with standard input or standard output:

      cat my-file | gs cp - gs://my-bucket/my-file

      gs cp gs://my-bucket/my-file.json - | jq .

    Wildcard globs (*) are supported only at the end of gs:// paths.
    """
    assert len(paths) >= 2
    paths = [os.path.expanduser(p) for p in paths]
    if all(p.startswith("gs://") for p in paths):
        dest_bucket, dest_prefix = parse_bucket_and_prefix(paths[-1])
        for path in paths[:-1]:
            for source_bucket, item in expand_trailing_glob(*parse_bucket_and_prefix(path)):
                source_key, dest_key = item["name"], dest_prefix
                # TODO: check if dest_prefix is a prefix on the remote
                if dest_prefix.endswith("/") or path.endswith("*") or len(paths) > 2:
                    dest_key = os.path.join(dest_prefix, os.path.basename(source_key))
                copy_one_remote(source_bucket=source_bucket, source_key=source_key,
                                dest_bucket=dest_bucket, dest_key=dest_key)
    elif all(p.startswith("gs://") for p in paths[:-1]) and not paths[-1].startswith("gs://"):
        for path in paths[:-1]:
            for source_bucket, item in expand_trailing_glob(*parse_bucket_and_prefix(path)):
                dest_filename = paths[-1]
                if os.path.isdir(dest_filename) or len(paths) > 2:
                    dest_filename = os.path.join(dest_filename, os.path.basename(item["name"]))
                download_one_file(bucket=source_bucket, key=item["name"], dest_filename=dest_filename)
    elif paths[-1].startswith("gs://") and not any(p.startswith("gs://") for p in paths[0:-1]):
        for path in paths[:-1]:
            if path.endswith(".gsdownload"):
                logger.info("Skipping partial download file %s", path)
                continue
            dest_bucket, dest_prefix = parse_bucket_and_prefix(paths[-1])
            dest_key = dest_prefix
            # TODO: check if dest_prefix is a prefix on the remote
            if dest_prefix == "" or dest_prefix.endswith("/") or len(paths) > 2:
                dest_key = os.path.join(dest_prefix, os.path.basename(path))
            upload_one_file(path, dest_bucket, dest_key, **upload_metadata_kwargs)
    else:
        raise click.BadParameter("paths")

cli.add_command(cp)

@click.command()
@click.argument('paths', nargs=-1, required=True)
@format_http_errors
def mv(paths):
    """Move files to, from, or between buckets."""
    cp.main(paths, standalone_mode=False)
    rm.main(paths[:-1], standalone_mode=False)

cli.add_command(mv)

def batch_delete_prefix(bucket, prefix, max_workers, dryrun=False, recurse_into_dirs=True, require_separator="/"):
    list_params = dict()
    if prefix and require_separator and not prefix.endswith(require_separator):
        prefix += require_separator
    if not recurse_into_dirs:
        list_params["delimiter"] = "/"
        prefix = prefix.rstrip("*")
    if prefix:
        list_params["prefix"] = prefix
    items = client.list("b/{}/o".format(bucket), params=list_params, include_prefixes=False)
    futures, total = [], 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as threadpool:
        for batch in batches(items, batch_size=100):
            action = "Would delete" if dryrun else "Deleting"
            logger.info("%s batch of %d objects in gs://%s/%s", action, len(batch), bucket, prefix)
            futures.append(threadpool.submit(batch_client.post_batch, [
                requests.Request(method="DELETE",
                                 url="b/{bucket}/o/{key}".format(bucket=requests.compat.quote(bucket),
                                                                 key=requests.compat.quote(obj_desc["name"], safe="")),
                                 params=dict(ifGenerationMatch="0") if dryrun else dict())
                for obj_desc in batch
            ], expect_codes=[requests.codes.precondition_failed] if dryrun else None))
        for future in futures:
            total += len(future.result())
    return total

@click.command()
@click.argument('paths', nargs=-1, required=True)
@click.option("--recursive", is_flag=True,
              help="If a given path is a directory (prefix), delete all objects sharing that prefix.")
@click.option("--max-workers", type=int, default=cpu_count(),
              help="Limit batch delete concurrency to this many threads (default: number of CPU cores detected)")
@click.option("--dryrun", is_flag=True, help="List the operations that would run without actually running them.")
@format_http_errors
def rm(paths, recursive=False, max_workers=None, dryrun=False):
    """
    Delete objects (files) from buckets.

    Wildcard globs (*) are supported only at the end of gs:// paths.
    """
    if not all(p.startswith("gs://") for p in paths):
        raise click.BadParameter("All paths must start with gs://")
    num_deleted = 0
    for path in paths:
        bucket, prefix = parse_bucket_and_prefix(path)
        print("{} gs://{bucket}/{key}".format("Would delete" if dryrun else "Deleting", bucket=bucket, key=prefix))
        try:
            client.delete("b/{bucket}/o/{key}".format(bucket=requests.compat.quote(bucket),
                                                      key=requests.compat.quote(prefix, safe="")),
                          params=dict(ifGenerationMatch="0") if dryrun else dict())
            num_deleted += 1
        except requests.exceptions.HTTPError as e:
            if dryrun and e.response is not None and e.response.status_code == requests.codes.precondition_failed:
                num_deleted += 1
            elif e.response is not None and e.response.status_code == requests.codes.not_found:
                if recursive:
                    num_deleted += batch_delete_prefix(bucket, prefix, max_workers=max_workers, dryrun=dryrun)
                elif prefix.endswith("*"):
                    num_deleted += batch_delete_prefix(bucket, prefix, max_workers=max_workers, dryrun=dryrun,
                                                       recurse_into_dirs=False, require_separator=None)
                else:
                    msg = '{}. To recursively delete directories (prefixes), use "gs rm --recursive PATH".'
                    raise Exception(msg.format(e.response.json()["error"]["message"]))
            else:
                raise
    print("Done. {} objects {}deleted.".format(num_deleted, "would be " if dryrun else ""))
cli.add_command(rm)

@click.command()
@click.argument('paths', nargs=2, required=True)
@click.option("--max-workers", type=int, default=cpu_count(),
              help="Limit upload/download concurrency to this many threads (default: number of CPU cores detected)")
@format_http_errors
def sync(paths, max_workers=None):
    """Sync a directory of files with bucket/prefix."""
    src, dest = [os.path.expanduser(p) for p in paths]
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as threadpool:
        if src.startswith("gs://") and not dest.startswith("gs://"):
            bucket, prefix = parse_bucket_and_prefix(src)
            prefix = prefix.rstrip("*")
            list_params = dict(prefix=prefix) if prefix else dict()
            items = client.list("b/{}/o".format(bucket), params=list_params)
            for remote_object in items:
                assert ".." not in remote_object["name"].split("/")
                try:
                    local_path = os.path.join(dest, remote_object["name"])
                    local_size = get_file_size(local_path)
                    local_mtime = datetime.datetime.utcfromtimestamp(os.path.getmtime(local_path))
                    remote_mtime = dateutil_parse(remote_object["updated"]).replace(tzinfo=None, microsecond=0)
                    if local_size == int(remote_object["size"]) and remote_mtime <= local_mtime:
                        logger.debug("sync:%s:%s: size/mtime match, skipping", src, local_path)
                        continue
                except OSError:
                    pass
                makedirs(os.path.dirname(local_path), exist_ok=True)
                futures.append(threadpool.submit(download_one_file, bucket, remote_object["name"], local_path))
        elif dest.startswith("gs://") and not src.startswith("gs://"):
            bucket, prefix = parse_bucket_and_prefix(dest)
            list_params = dict(prefix=prefix) if prefix else dict()
            remote_objects = {i["name"]: i for i in client.list("b/{}/o".format(bucket), params=list_params)}
            for root, dirs, files in os.walk(src):
                for filename in files:
                    if filename.endswith(".gsdownload"):
                        logger.info("Skipping partial download file %s", filename)
                        continue
                    local_path = os.path.join(root, filename)
                    local_size = get_file_size(local_path)
                    local_mtime = datetime.datetime.utcfromtimestamp(os.path.getmtime(local_path))
                    remote_path = os.path.join(prefix, os.path.relpath(root, src).lstrip("./"), filename)
                    try:
                        remote_object = remote_objects[remote_path]
                        remote_mtime = dateutil_parse(remote_object["updated"]).replace(tzinfo=None, microsecond=0)
                        if local_size == int(remote_object["size"]) and remote_mtime >= local_mtime:
                            logger.debug("sync:%s:%s: size/mtime match, skipping", local_path, dest)
                            continue
                    except KeyError:
                        pass
                    futures.append(threadpool.submit(upload_one_file, local_path, bucket, remote_path))
        else:
            raise click.BadParameter("Expected a local directory and a gs:// URL or vice versa")

        for future in futures:
            future.result()

cli.add_command(sync)

@click.command()
@click.argument('path', required=True)
@click.option('--expires-in', type=Timestamp, default="1h",
              help=('Time when or until the presigned URL expires. Examples: 60s, 5m, 1h, 2d, 3w, 2020-01-01, 15:20, '
                    '1535651591 (seconds since epoch). Default 1h.'))
def presign(path, expires_in=Timestamp("1h")):
    """Get a pre-signed URL for accessing an object."""
    bucket, key = parse_bucket_and_prefix(path)
    print(client.get_presigned_url(bucket, key, expires_at=expires_in.timestamp()))

cli.add_command(presign)

@click.command()
@click.argument('bucket_name')
@click.option('--location')
@click.option('--storage-class', type=click.Choice(choices=["STANDARD", "MULTI_REGIONAL", "NEARLINE", "COLDLINE",
                                                            "DURABLE_REDUCED_AVAILABILITY"]))
@format_http_errors
def mb(bucket_name, storage_class=None, location=None):
    """Create a new Google Storage bucket."""
    logger.info("Creating new Google Storage bucket {}".format(bucket_name))
    api_params = dict(name=bucket_name)
    if location:
        api_params["location"] = location
    if storage_class:
        api_params["storageClass"] = storage_class
    res = client.post("b", params=dict(project=client.get_project()), json=api_params)
    print(json.dumps(res, indent=4))

cli.add_command(mb)

@click.command()
@click.argument('bucket_name')
@format_http_errors
def rb(bucket_name):
    """Permanently delete an empty bucket."""
    print("Deleting Google Storage bucket {}".format(bucket_name))
    client.delete("b/{}".format(requests.compat.quote(bucket_name)))

cli.add_command(rb)

@click.command()
@click.argument('method')
@click.argument('gs_url')
@click.argument('args', nargs=-1)
def api(method, gs_url, args):
    """
    Use httpie to perform a raw HTTP API request.

    Example:

      gs api head gs://my-bucket/my-blob
    """
    bucket, prefix = parse_bucket_and_prefix(gs_url, require_gs_uri=False)
    path = "b/{bucket}".format(bucket=requests.compat.quote(bucket))
    args = list(args) + ["Authorization: Bearer " + client.get_oauth2_token(), "--check-status"]
    if prefix:
        path += "/o/{key}".format(key=requests.compat.quote(prefix, safe=""))
    try:
        os.execvp("http", ["http", method, client.base_url + path] + args)
    except EnvironmentError:
        exit("Error launching http. Please ensure httpie is installed (pip install httpie).")

cli.add_command(api)

client = GSClient()
upload_client = GSUploadClient(config=client.config)
batch_client = GSBatchClient(config=client.config)
