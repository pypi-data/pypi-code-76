import argparse
import time
import json
import boto3
from jwcrypto import jwk, jwt


class Ssm:
    def __init__(self):
        self.ssm = boto3.client("ssm")

    def get_encrypted_param(self, name):
        param = self.ssm.get_parameter(Name=name, WithDecryption=True)
        value = param["Parameter"]["Value"]
        return value


def create_signed_token(param_path: str, claims: dict):
    ssm = Ssm()
    param_full = json.loads(ssm.get_encrypted_param(param_path))
    claims["iss"] = param_full["issuer"]
    param_key = param_full["key"]
    key = jwk.JWK.from_json(param_key)
    token = jwt.JWT(header={"alg": "RS256", "kid": key.key_id}, claims=claims)
    token.make_signed_token(key)
    astext = token.serialize()
    return astext


def create_default_claims():
    return {
        # issued at
        "iat": str(int(time.time())),
        # expires at
        "exp": str(int(time.time() + 60 * 60 * 24)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ssm",
        default="/keykeeper/1",
        help="SSM parameter path to read secret key from",
    )
    reserved_claims = ["aud", "sub"]
    parser.add_argument(
        "--claim",
        help="Add custom claim, in format --claim shoesize=43",
        action="append",
    )
    for arg in reserved_claims:
        parser.add_argument("--" + arg, help=f"Reserved claim '{arg}'")

    parsed = parser.parse_args()

    claims = create_default_claims()

    claims.update(
        {
            k: v
            for (k, v) in vars(parsed).items()
            if k in reserved_claims and v is not None
        }
    )
    for claim in parsed.claim if parsed.claim else []:
        assert "=" in claim
        l, r = claim.split("=", 1)
        claims[l] = r
    token = create_signed_token(parsed.ssm, claims)
    print(token)


if __name__ == "__main__":
    main()
