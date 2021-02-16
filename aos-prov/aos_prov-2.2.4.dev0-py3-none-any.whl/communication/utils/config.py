#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from aos_prov.communication.utils.unit_certificate import UnitCertificate


class Config(object):
    """ Contains a provisioning procedure configuration. """

    def __init__(self):
        self._system_id = None
        self._model_name = None
        self._model_version = None
        self._user_claim = None
        self._supported_cert_types = None
        self._unit_certificates = []

    @property
    def system_id(self) -> str:
        return self._system_id

    @system_id.setter
    def system_id(self, value):
        self._system_id = value

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def model_version(self) -> str:
        return self._model_version

    @property
    def supported_cert_types(self) -> [str]:
        return self._supported_cert_types

    @supported_cert_types.setter
    def supported_cert_types(self, value):
        self._supported_cert_types = value

    @property
    def unit_certificates(self) -> [UnitCertificate]:
        return self._unit_certificates

    @unit_certificates.setter
    def unit_certificates(self, value):
        self._unit_certificates = value

    def set_model(self, model_string):
        model_chunks = model_string.strip().split(";")
        self._model_name = model_chunks[0].strip()
        if len(model_chunks) > 1:
            self._model_version = model_chunks[1].strip()
        else:
            self._model_version = "Unknown"
