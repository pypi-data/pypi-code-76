#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

class UnitCertificate(object):

    def __init__(self):
        self._cert_type = None
        self._csr = None
        self._certificate = None

    @property
    def cert_type(self) -> str:
        return self._cert_type

    @cert_type.setter
    def cert_type(self, value):
        self._cert_type = value

    @property
    def csr(self) -> str:
        return self._csr

    @csr.setter
    def csr(self, value):
        self._csr = value

    @property
    def certificate(self) -> str:
        return self._certificate

    @certificate.setter
    def certificate(self, value):
        self._certificate = value
