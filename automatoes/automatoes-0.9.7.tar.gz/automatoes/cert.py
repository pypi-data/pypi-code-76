#!/usr/bin/env python
#
# Copyright 2019-2020 Flavio Garcia
# Copyright 2016-2017 Veeti Paananen under MIT License
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Cryptography, hopefully mostly correct.
"""

import logging

from cryptography import x509
from cryptography.x509 import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives import hashes

import re

logger = logging.getLogger(__name__)


def create_csr(key, domains, must_staple=False):
    """
    Create a CSR in DER format for the specified key and domain names.
    """
    assert domains
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, domains[0]),
    ])
    san = x509.SubjectAlternativeName(
        [x509.DNSName(domain) for domain in domains])
    csr = (x509.CertificateSigningRequestBuilder()
           .subject_name(name).add_extension(san, critical=False))
    if must_staple:
        ocsp_must_staple = x509.TLSFeature(
            features=[x509.TLSFeatureType.status_request])
        csr = csr.add_extension(ocsp_must_staple, critical=False)
    return csr.sign(key, hashes.SHA256(), default_backend())


def load_csr(data):
    """
    Loads a PEM X.509 CSR.
    """
    return x509.load_pem_x509_csr(data, default_backend())


def load_der_certificate(data):
    """
    Loads a DER X.509 certificate.
    """
    return x509.load_der_x509_certificate(data, default_backend())


def load_pem_certificate(data):
    """
    Loads a PEM X.509 certificate.
    """
    return x509.load_pem_x509_certificate(data, default_backend())


def get_certificate_domain_name(cert):
    return cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value


def get_certificate_domains(cert):
    """
    Gets a list of all Subject Alternative Names in the specified certificate.
    """
    for ext in cert.extensions:
        ext = ext.value
        if isinstance(ext, x509.SubjectAlternativeName):
            return ext.get_values_for_type(x509.DNSName)
    return []


def export_pem_certificate(cert):
    """
    Exports a X.509 certificate as PEM.
    """
    return cert.public_bytes(Encoding.PEM)


def strip_certificates(data):
    p = re.compile("-----BEGIN CERTIFICATE-----\n(?s).+?"
                   "-----END CERTIFICATE-----\n")
    stripped_data = []
    for cert in p.findall(data.decode()):
        stripped_data.append(cert.encode())
    return stripped_data
