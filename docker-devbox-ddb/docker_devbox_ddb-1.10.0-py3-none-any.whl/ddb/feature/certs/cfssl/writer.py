# -*- coding: utf-8 -*-
"""
Writer module
"""

from os.path import normpath, expanduser, expandvars, join

from .checksums import validate_checksum
from .crypto import convert_pem_to_der


def _write_file(path, binary, destination=None):
    if destination:
        path = join(normpath(expandvars(expanduser(destination))), path)
    with open(path, 'wb') as stream:
        stream.write(binary)
    return path


def get_certs_path(output, conf=None, destination=None):
    """
    Get paths of certificate files generated by this module
    """
    if not conf:
        conf = {}

    filenames = conf.get('filenames', {})
    if not destination:
        destination = conf.get('destination')

    private_key_path = filenames.get('private_key', '%s.key.pem') % output
    certificate_path = filenames.get('certificate', '%s.pem') % output

    if destination:
        private_key_path = join(normpath(expandvars(expanduser(destination))), private_key_path)
        certificate_path = join(normpath(expandvars(expanduser(destination))), certificate_path)

    return certificate_path, private_key_path


def write_files(response, output, der, csr, conf=None, destination=None, append_ca_certificate=False, client=None,
                verify_checksum=True):
    """
    Write files contained in response.
    :param response:
    :param output:
    :type output: str
    :param der:
    :param csr:
    :param conf:
    :param append_ca_certificate:
    :param destination:
    :param client:
    """
    # pylint: disable=too-many-locals,too-many-branches
    if not conf:
        conf = {}

    certificate_der = None
    certificate_request_der = None

    should_verify_certificate_der = True

    filenames = conf.get('filenames', {})
    if not destination:
        destination = conf.get('destination')

    generated = {}
    if 'private_key' in response:
        private_key = response['private_key'].encode('ascii')
        generated['private_key'] = \
            _write_file(filenames.get('private_key', '%s.key.pem') % output, private_key, destination=destination)

    if 'certificate' in response:
        certificate = response['certificate'].encode('ascii')
        certificate_der = convert_pem_to_der('certificate', certificate)
        if verify_checksum:
            validate_checksum('certificate', certificate_der, response['sums']['certificate'], True)

        if append_ca_certificate and client:
            info = client.info('')

            ca_cert = info['certificate'] + '\n'

            certificate += ca_cert.encode('ascii')
            certificate_der = convert_pem_to_der('certificate', certificate)
            should_verify_certificate_der = False

        generated['certificate'] = \
            _write_file(filenames.get('certificate', '%s.pem') % output, certificate, destination=destination)
    if csr and 'certificate_request' in response:
        certificate_request_der = convert_pem_to_der('certificate_request',
                                                     response['certificate_request'].encode('ascii'))
        if verify_checksum:
            validate_checksum('certificate_request', certificate_request_der,
                              response['sums']['certificate_request'], True)
        generated['certificate_request'] = \
            _write_file(filenames.get('certificate_request', '%s.csr.pem') % output,
                        response['certificate_request'].encode('ascii'),
                        destination=destination)

    if der:
        if 'certificate' in response:
            generated['certificate_der'] = \
                _write_file(filenames.get('certificate_der', '%s.der') % output,
                            certificate_der,
                            destination=destination)
            if verify_checksum and should_verify_certificate_der:
                with open(filenames.get('certificate_der', '%s.der') % output, 'rb') as der_file:
                    content = der_file.read()
                    validate_checksum('certificate', content, response['sums']['certificate'], True)
        if csr and 'certificate_request' in response:
            generated['certificate_request_der'] = \
                _write_file(filenames.get('certificate_request_der', '%s.csr.der') % output,
                            certificate_request_der,
                            destination=destination)
            if verify_checksum:
                with open(filenames.get('certificate_request_der', '%s.csr.der') % output, 'rb') as der_file:
                    content = der_file.read()
                    validate_checksum('certificate_request', content, response['sums']['certificate_request'], True)
    return generated


def write_stdout(response, der, csr, append_ca_certificate, client=None):
    """
    Writes certificates to stdout.
    :param response:
    :param der:
    :param csr:
    :param append_ca_certificate:
    :param client:
    :return:
    """
    if 'private_key' in response:
        print(response['private_key'])
    if 'certificate' in response:
        print(response['certificate'])

        if append_ca_certificate and client:
            info = client.info('')
            ca_cert = info['certificate'] + '\n'
            print(ca_cert)

    if 'certificate_request' in response:
        print(response['certificate_request'])

    if der:
        if 'certificate' in response:
            print(convert_pem_to_der('certificate', response['certificate']))
        if csr and 'certificate_request' in response:
            print(convert_pem_to_der('certificate_request', response['certificate_request']))
