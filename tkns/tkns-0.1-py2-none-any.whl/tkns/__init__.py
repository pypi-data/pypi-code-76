import secrets

def token(nBytes=16):
    return secrets.token_hex(nBytes)