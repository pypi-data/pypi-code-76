import typer
import pathlib
import logging
from .core import upload_file
import os
import boto3
import tempfile
import piphyperd

s3_bucket = os.environ["S3_PYPI"]
app = typer.Typer()

@app.command("hello")
def hello_there():
    print("hello world")


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

    
@app.command("install")
def download_install(package_name: str):
    package_path = f"{s3_bucket}/{package_name}"
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(
        Bucket = s3_bucket,
        Prefix = package_name
            )
    package_key = response["Contents"][0]["Key"]
    wheel_name = package_key.split("/")[-1]
    print(package_key)
    temp_dir = tempfile.TemporaryDirectory()
    s3.download_file(
            Bucket=s3_bucket,
            Key= package_key,
            Filename = f"{temp_dir.name}/{wheel_name}")
    print(f"Downloaded package to {temp_dir.name}")
    piphyperd.PipHyperd().install(f"{temp_dir.name}/{wheel_name}")

def main():
    app()
