import hashlib


def get_sha256(text: str, salt: str = "", iterations: int = 10000) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=text.encode(encoding="utf-8"),
        salt=salt.encode(),
        iterations=iterations,
    )
