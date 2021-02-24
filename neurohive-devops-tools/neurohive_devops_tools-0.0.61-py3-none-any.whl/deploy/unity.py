import io
import os
import base64
import logging

import OpenSSL
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from neurohive.integration.appstoreconnect import AppStoreConnect
from neurohive.integration.unitycloud import UnityCloud


logger = logging.getLogger()


def _prep_p12(secret: str):
    SIGN_KEY_DATA = base64.b64decode(os.environ['SIGN_KEY_DATA_B64'])
    SIGN_CERT_DATA = base64.b64decode(os.environ['SIGN_CERT_DATA_B64'])

    certificate = x509.load_der_x509_certificate(SIGN_CERT_DATA, default_backend())
    private_key = serialization.load_pem_private_key(
        SIGN_KEY_DATA,
        password=None,
        backend=default_backend()
    )
    pkcs12 = OpenSSL.crypto.PKCS12()
    pkcs12.set_certificate(OpenSSL.crypto.X509.from_cryptography(certificate))
    pkcs12.set_privatekey(OpenSSL.crypto.PKey.from_cryptography_key(private_key))
    return pkcs12.export(secret.encode('utf-8'))


def update_unity_ios_creds(project, target, bundle_id, prov_type):
    apple = AppStoreConnect()
    bundle = apple.get_bundle(bundle_id, prov_type)
    sign_key_secret = 'secret'
    sign_key = io.BytesIO(_prep_p12(sign_key_secret))
    prov_strem = io.BytesIO(bundle.prov_data)
    uc = UnityCloud('unity_oekd8fheerjomw', project)
    creds_id = uc.upload_ios_credentials(bundle_id, sign_key, prov_strem, sign_key_secret)
    uc.update_ios_app_creds(target, creds_id)


if __name__ == '__main__':
    # update_unity_ios_creds('MIB', 'Stage cheats iOS', 'io.neurohive.bncstagecheats', 'adhoc')
    update_unity_ios_creds('MIB', 'Prod iOS',
                           'rocks.mpgames.blastconquer', 'appstore')
