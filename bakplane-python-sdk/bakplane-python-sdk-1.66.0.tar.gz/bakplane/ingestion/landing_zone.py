import logging
import gzip
import os
import shutil
import tempfile
import glob

from abc import ABC, abstractmethod
from urllib.parse import urlparse

import boto3
import typing


class LandingZone(ABC):
    @abstractmethod
    def upload(
        self,
        src_path: str,
        dst_path: str,
        suffix: str = "",
        prefix: str = None,
    ):
        pass

    @abstractmethod
    def list_files(self, bucket: str, prefix: str) -> typing.List[str]:
        pass

    @abstractmethod
    def download_file_into(
        self, bucket: str, prefix: str, f
    ) -> typing.List[str]:
        pass


class FilesystemLandingZone(LandingZone):
    def list_files(self, bucket: str, prefix: str) -> typing.List[str]:
        return glob.glob(os.path.join(bucket, prefix), recursive=True)

    def download_file_into(
        self, bucket: str, prefix: str, f
    ) -> typing.List[str]:
        with open(os.path.join(bucket, prefix), "r+b") as f_in:
            shutil.copyfileobj(f_in, f)

    def upload(
        self,
        src_path: str,
        dst_path: str,
        suffix: str = "",
        prefix: str = None,
    ):
        u = urlparse(dst_path)

        p = u.path
        if prefix:
            p = os.path.join(p, prefix) + "/"

        if not os.path.exists(p):
            os.makedirs(p)

        with open(src_path, "rb") as f_in:
            with tempfile.NamedTemporaryFile(
                "wb",
                prefix=p,
                delete=False,
                suffix=suffix,
            ) as f:
                with gzip.open(f, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    logging.info(f"Artifact written to `{f.name}`")


class AmazonS3LandingZone(LandingZone):
    def __init__(self):
        self.client = boto3.client("s3")

    def list_files(self, bucket: str, prefix: str) -> typing.List[str]:
        kwargs = {"Bucket": bucket, "Prefix": prefix}
        while True:
            resp = self.client.list_objects_v2(**kwargs)
            for obj in resp["Contents"]:
                yield obj["Key"]
            try:
                kwargs["ContinuationToken"] = resp["NextContinuationToken"]
            except KeyError:
                break

    def download_file_into(self, bucket: str, key: str, f) -> typing.List[str]:
        return self.client.download_fileobj(bucket, key, f)

    def upload(
        self,
        src_path: str,
        dst_path: str,
        suffix: str = "",
        prefix: str = None,
    ):
        u = urlparse(dst_path)

        if u.scheme != "s3":
            raise RuntimeError("Invalid destination path.")

        with open(src_path, "rb") as f_in:
            f = tempfile.NamedTemporaryFile(
                delete=False, prefix=os.path.basename(src_path)
            )
            final_path = f.name

            with gzip.open(f, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

            f.close()

            self.client.upload_file(
                final_path,
                u.netloc,
                u.path[1:] + os.path.basename(src_path) + suffix,
            )


class LandingZoneFactory(object):
    @staticmethod
    def build_from_code(code):
        if code == "s3":
            return AmazonS3LandingZone()
        elif code == "file":
            return FilesystemLandingZone()
        raise RuntimeError(
            f"Could not find landing zone matching scheme `{u.scheme}`."
        )

    @staticmethod
    def build_from_uri(uri):
        u = urlparse(uri)

        if u.scheme == "s3":
            return AmazonS3LandingZone()
        elif u.scheme == "file":
            return FilesystemLandingZone()
        raise RuntimeError(
            f"Could not find landing zone matching scheme `{u.scheme}`."
        )
