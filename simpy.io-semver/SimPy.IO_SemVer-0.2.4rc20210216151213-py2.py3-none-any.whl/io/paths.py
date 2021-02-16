from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent
TEST_SECRETS_DIR_PATH = ROOT_PATH / 'test' / 'secrets'
KEY_FILE_PATH = str(TEST_SECRETS_DIR_PATH / 'server.key.pem')
CERT_FILE_PATH = str(TEST_SECRETS_DIR_PATH / 'certificate.pem')
