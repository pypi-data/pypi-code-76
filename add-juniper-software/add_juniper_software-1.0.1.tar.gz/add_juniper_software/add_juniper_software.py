#!/usr/bin/env python3
"""
add_juniper_software
~~~~~~~~~~~~~~~~~~~~
Uploads and installs the provided software candidate on the specified JunOS switch.
"""

# Third-party libraries.
import click
from getpass import getpass
import paramiko

@click.command(
    help="uploads and installs the provided software candidate on the specified JunOS switch."
)
@click.argument(
    'ip_address',
    type=str
)
@click.argument(
    'install_file',
    type=str
)
@click.option(
    '-c',
    '--clean_install',
    is_flag=True,
    help='remove old version of software before installing'
)
@click.option(
    '-k',
    '--ssh_keyfile',
    type=str,
    default='',
    help='the SSH keyfile for the the switch'
)
@click.option(
    '-l',
    '--upload_location',
    type=str,
    default='/tmp/',
    help='the location on the switch where the installation candidate will be uploaded'
)
@click.option(
    '-n',
    '--software_name',
    type=str,
    default='',
    help='the name of the software to remove for clean install'
)
@click.option(
    '-p',
    '--password',
    type=str,
    default='',
    help='the SSH password for the switch'
)
@click.option(
    '-u',
    '--username',
    type=str,
    default='',
    help='the SSH username for the switch'
)
@click.help_option(
    '-h',
    '--help',
    help='show this message and exit'
)
def add_juniper_software(
    ip_address,
    install_file,
    password='',
    username='',
    ssh_keyfile='',
    clean_install=False,
    software_name='',
    upload_location='/tmp/'
):
    """
    Uploads and installs the provided software candidate on the specified JunOS switch.

    :param ip_address:      The IP address of the switch to install the software on.
    :type ip_address:       ``str``
    :param install_file:    The qualified path to the installation file.
    :type install_file:     ``str``
    :param password:        (optional) The SSH password for the switch OR, if ``ssh_keyfile`` is
                            provided, the password to unlock the key. If left blank and
                            ``ssh_keyfile`` is not provided, the password will be prompted with the
                            ``getpass`` library. Defaults to ``""``.
    :type password:         ``str``
    :param username:        (optional) The SSH username for the switch. If left blank, the username
                            will be prompted. Defaults to ``""``.
    :type username:         ``str``
    :param ssh_keyfile:     (optional) The qualified path to an SSH keyfile. Usually this would be
                            ``~/.ssh/id_rsa.pub`` or similar on a Unix type system. Defaults to
                            ``""``.
    :type ssh_keyfile:      ``str``
    :param clean_install:   (optional) Whether the old version of the target software should be
                            removed prior to installing the new software. If this flag is set to
                            ``True``, then the ``software_name`` parameter must be set, otherwise a
                            ``ValueError`` will be raised. Defaults to ``False``.
    :type clean_install:    ``bool``
    :param software_name:   (optional) The name of the software to be removed prior to a clean
                            install. If ``clean_install`` is ``False``, then this flag will be
                            ignored. Defaults to ``""``.
    :type software_name:    ``str``
    :param upload_location: (optional) The directory on the JunOS switch to upload the software to.
                            Defaults to ``""``.
    :type upload_location:  ``str``
    :return:                Nothing.
    :rtype:                 ``None``
    """
    # Get username and password if not provided.
    if username == '':
        username = input("Enter SSH username for " + str(ip_address) + ":\t")
    if password == '' and ssh_keyfile == '':
        while True:
            password = getpass("Enter SSH password for " + str(ip_address) + ":\t")
            if password == getpass("Enter SSH password again:\t\t"):
                break
            print("Passwords do no match!")
    # Validate input.
    if clean_install and software_name == "":
        raise ValueError(
            "software_name flag must be set when clean_install is True"
        )
    if upload_location[-1] != "/":
        upload_location += "/"

    # Get filename from ``install_file``.
    filename = install_file.split("/")[-1]

    # Configure and connect SFTP/SSH clients.
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    transport = paramiko.Transport((ip_address, 22))
    if ssh_keyfile != "" and password != "":
        ssh.connect(ip_address, username=username, password=password, key_filename=ssh_keyfile)
        transport.connect(hostkey=ssh_keyfile, username=username, password=password)
    elif ssh_keyfile != "":
        ssh.connect(ip_address, username=username, key_filename=ssh_keyfile)
        transport.connect(hostkey=ssh_keyfile, username=username)
    else:
        ssh.connect(ip_address, username=username, password=password)
        transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Upload file to switch.
    print("Uploading installation candidate....")
    sftp.put(install_file, upload_location + filename)
    
    # Optionally remove old version of software.
    if clean_install:
        print("Removing old version....")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('request system software delete ' + software_name)
        for line in ssh_stdout.readlines():
            print(line)

    # Install update.
    print("Installing....")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('request system software add ' + upload_location + filename)
    for line in ssh_stdout.readlines():
        print(line)

    # Close connections.
    if ssh:
        ssh.close()
    if sftp:
        sftp.close()
    if transport:
        transport.close()
    print("....Done!")


if __name__ == "__main__":
    add_juniper_software()
