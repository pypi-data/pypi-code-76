import configparser
import os
import sqlite3
import sys
import unittest
from io import StringIO

from MyVault.src import Vault
from MyVault.src.statics import exit_codes
from MyVault.src.utils import AESEncryption

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class Test:
    DIR = os.path.join(CURRENT_DIR, "temp")

    def __init__(self):
        os.makedirs(self.DIR, exist_ok=True)

    def __del__(self):
        if os.path.exists(self.DIR) is True:
            if len(os.listdir(self.DIR)) == 0:
                os.removedirs(self.DIR)


class _Config(Test):

    SECTION = "cipher"
    CONFIG = {
        "key": "replace-me",
        "salt": "replace-me",
        "iterations": 10,
        "clipboard_ttl": 3,
    }

    def __init__(self, config_type: str):
        super().__init__()
        self.path = None
        self.data = None
        self.create_file(config_type=config_type)

    def create_file(self, config_type: str):
        config = configparser.ConfigParser()
        if config_type == "bad_key":
            config["bad_key"] = self.CONFIG
        elif config_type == "bad_value":
            self.CONFIG["iterations"] = "Ten"
            config[self.SECTION] = self.CONFIG
        else:
            config_type = "good"
            config[self.SECTION] = self.CONFIG

        self.path = os.path.join(self.DIR, f"{config_type}.cfg")
        self.data = config

        with open(file=self.path, mode="w") as config_file:
            config.write(fp=config_file)

    def __del__(self):
        if os.path.isfile(self.path) is True:
            os.remove(self.path)
        super().__del__()


class _Database(Test):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(self.DIR, "db.sqlite3")
        self.create_file()

    def create_file(self):
        conn = sqlite3.connect(self.path)
        conn.close()

    def __del__(self):
        if os.path.isfile(self.path) is True:
            os.remove(self.path)
        super().__del__()


class TestEncryptionConfig(unittest.TestCase):

    OUTPUT = StringIO()

    def test_01_good(self):
        sys.stdout = self.OUTPUT
        db = _Database()
        config = _Config(config_type="good")
        vault = Vault(db_path=db.path, config_path=config.path)
        sys.stdout = sys.__stdout__
        self.assertEqual(
            int(config.data["cipher"]["clipboard_ttl"]), vault.clipboard_ttl
        )

    def test_02_bad_key(self):
        sys.stdout = self.OUTPUT
        db = _Database()
        config = _Config(config_type="bad_key")
        with self.assertRaises(SystemExit) as err:
            _ = Vault(db_path=db.path, config_path=config.path)
        sys.stdout = sys.__stdout__
        self.assertEqual(err.exception.code, exit_codes.INVALID_KEY)

    def test_03_bad_value(self):
        sys.stdout = self.OUTPUT
        db = _Database()
        config = _Config(config_type="bad_value")
        with self.assertRaises(SystemExit) as err:
            _ = Vault(db_path=db.path, config_path=config.path)
        sys.stdout = sys.__stdout__
        self.assertEqual(err.exception.code, exit_codes.INVALID_VALUE)


class TestDatabase(unittest.TestCase):

    OUTPUT = StringIO()
    DB = _Database()
    CONFIG = _Config(config_type="good")
    CIPHER = AESEncryption(
        key=CONFIG.data["cipher"]["key"],
        salt=CONFIG.data["cipher"]["salt"],
        iterations=int(CONFIG.data["cipher"]["iterations"]),
    )

    FOLDER = "test_folder"
    NAME = "first"
    SECRET = "first_password"

    NONE_EXISTENT_FOLDER = "none_existent_folder"
    NONE_EXISTENT_NAME = "none_existent_name"

    def test_01_insert(self):
        sys.stdout = self.OUTPUT
        with Vault(db_path=self.DB.path, config_path=self.CONFIG.path) as vault:
            vault.upsert(folder=self.FOLDER, name=self.NAME, secret=self.SECRET)
            secret = vault.copy(folder=self.FOLDER, name=self.NAME, get=True)
            self.assertEqual(self.CIPHER.decrypt(ciphertext=secret), self.SECRET)
        sys.stdout = sys.__stdout__

    def test_02_none_existent_secret(self):
        sys.stdout = self.OUTPUT
        with self.assertRaises(SystemExit) as err:
            vault = Vault(db_path=self.DB.path, config_path=self.CONFIG.path)
            _ = vault.copy(
                folder=self.NONE_EXISTENT_FOLDER, name=self.NONE_EXISTENT_NAME, get=True
            )
        self.assertEqual(err.exception.code, exit_codes.SECRET_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
