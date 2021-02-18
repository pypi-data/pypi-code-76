import os

TEST_ROOT = os.path.dirname(__file__)
TEST_DATA = os.path.join(TEST_ROOT, 'data')

USE_VIRTUAL_DISPLAY = True
READ_FILE_TIMEOUT = 5


def read_file_binary(filepath: str) -> bytes:
    with open(filepath, 'rb') as file:
        return file.read()
