# Libraries
import logging
import os
import pathlib
import tempfile

import boto3
import piphyperd
import typer
from botocore.exceptions import ClientError

# Constants
environment = os.environ.get("DEPLOY_ENV")
s3_bucket = os.environ.get("S3_PYPI", "ds-sandbox-private-pypi")

if environment:
    session = boto3.Session(profile_name=environment)
else:
    session = boto3.Session()

s3_client = session.client("s3")
app = typer.Typer()


# Functions
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


@app.command("upload")
def upload_package(package_name: str):
    """
    run this command after you have build
    your package
    """
    try:
        wheel_path = next(pathlib.Path("./dist").glob("*.whl"))
        wheel_full_path = str(wheel_path.absolute())
        wheel_name = str(wheel_path.name)
        s3_key = f"{package_name}/{wheel_name}"
        print(f"Found wheel file in {wheel_full_path}")
        upload_file(wheel_full_path, s3_bucket, s3_key)
        print(f"uploaded to {s3_bucket}/{s3_key}")
    except StopIteration:
        print("No wheel file is found. Please build your package")


def download_install(package_name: str):
    package_path = f"{s3_bucket}/{package_name}"
    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=package_name)
        package_key = response["Contents"][0]["Key"]
        wheel_name = package_key.split("/")[-1]
        temp_dir = tempfile.TemporaryDirectory()
        s3_client.download_file(
            Bucket=s3_bucket, Key=package_key, Filename=f"{temp_dir.name}/{wheel_name}"
        )
        print(f"Downloaded package to {temp_dir.name}")
        piphyperd.PipHyperd().install(f"{temp_dir.name}/{wheel_name}")
    except:
        print(f"Can't find the packege {package_name}")


@app.command("install")
def install(
    packages: str,
    r: bool = typer.Option(False, "-r", "--recursive", help="install package from a file"),
):
    if r:
        with open(packages, "r") as f:
            packages = f.readlines()
            for p in packages:
                p = p.strip()
                download_install(p)
    else:
        download_install(packages)


def main():
    app()
