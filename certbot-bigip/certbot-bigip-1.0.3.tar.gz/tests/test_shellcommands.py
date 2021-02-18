"""
This test the deployment of several integration test
"""

import subprocess
import re
import logging
import ssl
import socket
import os

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger(__name__)
user = os.environ['BIGIP_USERNAME']
password = os.environ['BIGIP_PASSWORD']


def validate_certbot_certificate_delivery(stdout: str, stderr: str):
    # from https://www.regextester.com/96683
    regex_date = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
    regex_cert_expire_indicator = "(?<=Your certificate will expire on )"
    regex_check_result = regex_cert_expire_indicator + regex_date
    match = re.search(regex_check_result, stdout)
    if match is not None:
        mylogger.info(
            "New Certificate was created. Expiration Date:" + match.group(1))
        return True
    else:
        mylogger.error("Certificate aquirement failed: \n stdout:\n" + stdout + "\n sterr:\n" + stderr)
        return False


def get_certbot_certificate(domain: str):
    file_path = f"/etc/letsencrypt/live/{domain}/cert.pem"

    with open(file_path, 'r') as cert_file:
        return cert_file.read()


def is_delivered_cert_equal_deployed_cert(domain):
    # check if certificate has been deployed
    delivered_cert = get_certbot_certificate(domain)
    socket.setdefaulttimeout(5)  # set the timeout low to fail quickly if no certificate is served by the server

    # use sni in ssl communication
    port = 443
    conn = ssl.create_connection((domain, port))
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sock = context.wrap_socket(conn, server_hostname=domain)
    deployed_cert = ssl.DER_cert_to_PEM_cert(sock.getpeercert(True))
    mylogger.debug(f"delivered_cert: \n {delivered_cert}")
    mylogger.debug(f"deployed_cert: \n {deployed_cert}")
    return delivered_cert == deployed_cert


def test_response_evaluation():
    stdout_sample = 'IMPORTANT NOTES:\n - Congratulations! Your certificate and chain have been saved at:\n   /etc/letsencrypt/live/example1.on.at/fullchain.pem\n   Your key file has been saved at:\n   /etc/letsencrypt/live/example1.on.at/privkey.pem\n   Your certificate will expire on 2019-12-10.To obtain a new or tweaked\n   version of this certificate in the future, simply run certbot\n   again. To non-interactively renew *all* of your certificates, run\n   "certbot renew"\n'
    stderr_sample = ""
    validate_certbot_certificate_delivery(stdout_sample, stderr_sample)


def test_certbot_bigip_server_cert():
    domain = "test01.certbot.on.at"
    response = subprocess.run(
        ("certbot --non-interactive --expand --email 'certbot@ong.at' --agree-tos"
            " -a certbot-bigip:bigip -i certbot-bigip:bigip"
            " --certbot-bigip:bigip-list 'f5.ong.intern,f5-ha.ong.intern'"
            f" --certbot-bigip:bigip-username '{user}'"
            f" --certbot-bigip:bigip-password '{password}'"
            " --certbot-bigip:bigip-partition 'Intern'"
            " --certbot-bigip:bigip-clientssl-parent '/Common/ong_clientssl'"
            " --certbot-bigip:bigip-vs-list '/Intern/certbot.ong.at.app/certbot.ong.at_vs'"
            " --certbot-bigip:bigip-device-group 'fail-sync'"
            " --certbot-bigip:bigip-iapp '/Intern/certbot.ong.at.app/certbot.ong.at_vs'"
            f" -d {domain}"
            " -v --staging --debug --force-renewal"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    mylogger.debug(response.stdout.decode("utf-8"))

    # check if new certificate was created
    if not validate_certbot_certificate_delivery(response.stdout.decode("utf-8"), response.stderr.decode("utf-8")):
        assert False
    # check if process has finished correctly
    response.check_returncode()

    # check if certificate has been deployed
    assert is_delivered_cert_equal_deployed_cert(domain), "did you assign the ssl profile to the virtualserver? this step is not automated."


def test_certbot_bigip_deployment_in_custompartition_and_folders():
    domain = "test02.certbot.on.at"
    response = subprocess.run(
        ("certbot --non-interactive --expand --email 'certbot@ong.at' --agree-tos"
            " -a certbot-bigip:bigip -i certbot-bigip:bigip"
            " --certbot-bigip:bigip-list 'f5.ong.intern,f5-ha.ong.intern'"
            f" --certbot-bigip:bigip-username '{user}'"
            f" --certbot-bigip:bigip-password '{password}'"
            " --certbot-bigip:bigip-partition 'Common'"
            " --certbot-bigip:bigip-clientssl-parent '/Common/ong_clientssl'"
            " --certbot-bigip:bigip-vs-list '/AS3_Test/CERTBOT_TEST02/test02_certbot_on_at_80_vs,/AS3_Test/CERTBOT_TEST02/test02_certbot_on_at_443_vs'"
            " --certbot-bigip:bigip-device-group 'fail-sync'"
            f" -d {domain}"
            " -v --staging --debug --force-renewal"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # check if new certificate was created
    if not validate_certbot_certificate_delivery(response.stdout.decode("utf-8"), response.stderr.decode("utf-8")):
        assert False

    # check if process has finished correctly
    response.check_returncode()

    # check if certificate has been deployed
    assert is_delivered_cert_equal_deployed_cert(domain), "did you assign the ssl profile to the virtualserver? this step is not automated."


def test_wildcard_deployment_with_bluecat_validation():
    domain = "*.certbot.on.at"
    response = subprocess.run(
        (
            "certbot"
            " --non-interactive"
            f" -d {domain}"
            " --staging"
            " --expand"
            " --email 'certbot@ong.at'"
            " --agree-tos"
            " --no-eff-email"
            " -v"
            " --debug"
            " --force-renewal"

            # authentication
            " -a certbot-bluecat:bluecat"

            " -i certbot-bigip:bigip"
            " --certbot-bigip:bigip-list 'f5.ong.intern,f5-ha.ong.intern' "
            f" --certbot-bigip:bigip-username '{user}'"
            f" --certbot-bigip:bigip-password '{password}'"
            " --certbot-bigip:bigip-partition 'Intern' "
            " --certbot-bigip:bigip-clientssl-parent '/Common/ong_clientssl' "
            " --certbot-bigip:bigip-vs-list '/Intern/certbot.ong.at.app/certbot.ong.at_vs'"
            " --certbot-bigip:bigip-device-group 'fail-sync'"
            " --certbot-bigip:bigip-iapp '/Intern/certbot.ong.at.app/certbot.ong.at'"
        ),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )

    # check if new certificate was created
    if not validate_certbot_certificate_delivery(response.stdout.decode("utf-8"), response.stderr.decode("utf-8")):
        assert False

    # check if process has finished correctly
    response.check_returncode()

    # check if certificate has been deployed
    assert is_delivered_cert_equal_deployed_cert(domain.strip("*.")), "did you assign the ssl profile to the virtualserver? this step is not automated."
