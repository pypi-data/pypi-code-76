from nidhoggr.core.config import BLConfig
from nidhoggr.core.user import UserProperty
from nidhoggr.utils.crypto import sign_property, verify_property


def test_crypto(config: BLConfig):
    unsigned_prop = UserProperty(name="twilight", value="sparkle")
    signed_prop = sign_property(private_key=config.key_pair.private, prop=unsigned_prop)
    assert signed_prop is not None
    assert isinstance(signed_prop.signature, str)
    assert verify_property(public_key=config.key_pair.public, prop=signed_prop)
