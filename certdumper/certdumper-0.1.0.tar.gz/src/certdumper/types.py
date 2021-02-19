import json
from base64 import b64decode
from logging import getLogger
from pathlib import Path
from typing import List, Optional, Union

from certdumper import exc

import pydantic
L = getLogger(__name__)


class LetsEncryptAccountRegistrationBody(pydantic.BaseModel):
    status: str
    contact: List[str]


class LetsEncryptAccountRegistration(pydantic.BaseModel):
    uri: str
    body: LetsEncryptAccountRegistrationBody


class LetsEncryptAccount(pydantic.BaseModel):
    email: str = pydantic.Field(alias='Email')
    private_key: str = pydantic.Field(alias='PrivateKey')
    key_type: str = pydantic.Field(alias='KeyType')
    registration: LetsEncryptAccountRegistration = pydantic.Field(alias='Registration')


class AcmeCertDomain(pydantic.BaseModel):
    main: str


class AcmeCert(pydantic.BaseModel):
    domain: AcmeCertDomain
    certificate: str
    key: str
    store: str = pydantic.Field(alias="Store")

    class Config:
        allow_population_by_field_name = True

    @property
    def decoded_key(self) -> str:
        return b64decode(self.key).decode('utf-8')

    @property
    def decoded_cert(self) -> str:
        return b64decode(self.certificate).decode('utf-8')


class AcmeLetsEncrypt(pydantic.BaseModel):
    account: LetsEncryptAccount = pydantic.Field(alias='Account')
    certs: Optional[List[AcmeCert]] = pydantic.Field(alias='Certificates', default_factory=list)


class AcmeJson(pydantic.BaseModel):
    letsencrypt: AcmeLetsEncrypt

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> 'AcmeJson':
        with open(path) as fp:
            data = fp.read()

        if not data:
            raise exc.InvalidAcmeJson(path, data)

        try:
            values = json.loads(data)
            acme = cls(**values)
            return acme
        except Exception:
            raise exc.InvalidAcmeJson(path, data)


    def find_cert(self, domain: str) -> Optional[AcmeCert]:
        certs = self.letsencrypt.certs or []
        return next((x for x in certs if x.domain.main == domain), None)

