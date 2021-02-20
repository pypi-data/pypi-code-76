import sys, os
global save_stdout
save_stdout = sys.stdout
#############################################################################
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
def enablePrint():
    global save_stdout
    sys.stdout = save_stdout
    
class HiddenPrints:
    def __enter__(self):
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        global save_stdout
        sys.stdout = save_stdout
        
try:
    from cryptography.fernet import Fernet
except:
    os.system('pip install cryptography') 

try:
    from getpass import getpass
except:
    os.system('pip getpass')

##################################################################################################
# cryptography

import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
iterations = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)

def get_safe_pass():
  from getpass import getpass
  password = getpass(prompt = 'password:')
  return password

def encode_hub(message):
  token = password_encrypt(message.encode(), get_safe_pass()).decode('utf8')
  #print(token)
  return token

def decode_hub(token,password="-1"):
  try:
    if password == "-1":
        message = password_decrypt(token, get_safe_pass()).decode()
    else:
        message = password_decrypt(token, password).decode()
  except:
    message = Fernet.generate_key().decode('utf8')
  #print(message)
  return message
  
def safe_decode(token):
  with HiddenPrints():
      resposta = Fernet.generate_key().decode('utf8')
      try:
        message = password_decrypt(token, get_safe_pass()).decode()
        try:
            _locals = locals()
            exec(message, globals(), _locals)
        except:
            pass
      except:
        pass
  return resposta

#################################################################################################
