# ftp_down.py
# Dependencies: ftplib, pandas

import os.path
import ftplib
from motolib.errors import FTPConnectionError, FTPDownloadError, FTPEncodingError


def ftp_download(hostname, username, password, filename_filter, download_directory='.'):
    """
    ----------------------------------------------------------------
    Fetch information using FTP and save file to local machine.
    ----------------------------------------------------------------
    Parameters:
        hostname : string
            FTP host name
        username : string
            FTP login username
        password : string
            FTP login password
        filename_filter : string
            Name of file to download from FTP
        download_directory: string
            Directory to download file to. CWD is default
    Returns:
       NONE
    Side Effects:
        Writes and deletes feed file to local machine (in same dir as script)
            Output file will have same name as FTP file
            (ie. same as filename_filter parameter)
    ----------------------------------------------------------------
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
        ftp.encoding = "utf-8"
    except Exception as e:
        raise FTPEncodingError('Unable to enforce UTF-8 Encoding.')

    try:
        print(f"Starting Download of {filename_filter}...")
        # Downloads a copy of the FTP file, saving in current dir with same name as filename_filter
        ftp.retrbinary("RETR " + filename_filter, open(os.path.join(download_directory, filename_filter), 'wb').write)
        print("File Downloaded Successfully!\n")
        ftp.quit()

    except ftplib.error_perm as err:
        raise FTPDownloadError('Unable to open file.')
