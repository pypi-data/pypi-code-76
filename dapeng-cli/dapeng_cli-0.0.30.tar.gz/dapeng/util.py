import os
import logging
import datetime
from ftplib import FTP
import uuid
from base64 import b64decode
import click

from .settings import FTP_SER_HOST, FTP_CRED

LOGGER = logging.getLogger(__name__)

def upload_file(boardname, filepath):
    filename = os.path.basename(filepath)
    home_dir = 'Dapeng/dapeng-cli-bins'

    host = b64decode(FTP_SER_HOST).decode('utf-8')
    user = b64decode(FTP_CRED[0]).decode('utf-8')
    pwd = b64decode(FTP_CRED[1]).decode('utf-8')

    ftp = FTP(host)
    ftp.login(user, pwd)
    ftp.cwd('./')

    LOGGER.info("Upload <%s> to file server: %s.", filename, host)
    filename = os.path.basename(filepath)
    remote_dir = home_dir + '/' + str(uuid.uuid4()) + "_" + boardname
    remotefile = remote_dir + "/" + filename

    for fodlername in remote_dir.split('/'):
        if not fodlername:
            continue
        if fodlername not in ftp.nlst():
            ftp.mkd(fodlername)
        ftp.cwd(fodlername)

    filesize = os.path.getsize(filepath)
    with open(filepath, 'rb') as fileobj:
        with click.progressbar(length=filesize, label="progress") as bar:
            ftp.storbinary(
                'STOR %s' % filename,
                fileobj,
                1024,
                callback=lambda sent: bar.update(len(sent)))
    ftp.close()

    return "ftp://{user}:{pwd}@{host}/{path}".format(
        user=user,
        pwd=pwd,
        host=host,
        path=remotefile)
