import subprocess


def generate_private_key() -> str:
    return subprocess.check_output(["wg", "genkey"]).decode().strip()


def generate_public_key(private_key: str) -> str:
    return (
        subprocess.check_output(["wg", "pubkey"], input=private_key.encode())
        .decode()
        .strip()
    )


def generate_psk() -> str:
    return subprocess.check_output(["wg", "genpsk"]).decode().strip()
