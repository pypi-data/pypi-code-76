# up_ftp.py
# Dependencies: ftplib

import os
import ftplib
from motolib.errors import FTPConnectionError, FTPUploadError, FTPEncodingError

def ftp_upload_file(hostname, username, password, file_name, upload_name="NOUPLOADNAME"):
    """
    -------------------------------------------------------
    Uploads a given file to FTP
    -------------------------------------------------------
    Parameters:
        hostname : string
            FTP host name
        username : string
            FTP login username
        password : string
            FTP login password
        file_name : string
            Name of file in dir that will be uploaded
        upload_name : string
            !! MUST INCLUDE EXTENSION !!
            (Optional) Specifies name of FTP upload
                ie. can be uploaded with different name than local file
    Returns:
        True if supplement has been uploaded to FTP
        False if supplement did not upload to FTP
    ------------------------------------------------------
    """
    try:
        # Login to FTP
        print(f"Initializing FTP Download from {hostname}...")
        ftp = ftplib.FTP(hostname)
    except OSError:
        raise FTPConnectionError('Unable to establish connect to host')
    try:
        print("Attempting FTP Login...")
        ftp.login(username, password)
        print("FTP Login Successful!")
    except ftplib.error_perm as e:
        raise FTPConnectionError('Incorrect Login.')
    try:
        print(f"Starting Upload of {file_name}...")

        # Store file to FTP with appropriate upload name
        ftp.storbinary("STOR " + (file_name if upload_name == "NOUPLOADNAME" else upload_name), open(file_name, 'rb'))

        if upload_name == "NONE":
            print("File Upload Successful!")
        else:
            print(f"File Upload Successful! Saved on FTP as {upload_name}")

        ftp.quit()

    except ftplib.all_errors as err:
        raise FTPUploadError("ERROR: Could not upload to FTP.")
