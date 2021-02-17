"""
This module handles all the cryptography needed in this tool. It uses the
cryptography library to create private and public RSA keys of length 4096,
which is considered secure. In addition, we use the SHA256 hash algorithm in
the OAEP padding, which is also considered secure. Please note that any changes
in the cryptography of this module have to be associated with changes in
Jeeves, since it is the entity that encrypts the information.

Please note that the cryptography library we're using marks the RSA portion as
hazardous because they generally recommend consuming their RSA cryptography
through certificate generation. But that doesn't really fit our use case, so we
use RSA directly exactly as shown in their examples and certificate generation code. Since the
cryptography library is the most widely used Python crypto library, we prefer to use them since
their code is carefully scrutinized and maintained.
"""
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
    )
    public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode()
    return private_key, public_key_b64


def decrypt(encrypted_b64, private_key):
    encrypted = base64.b64decode(encrypted_b64)
    plaintext = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
        ),
    )
    return plaintext.decode()
