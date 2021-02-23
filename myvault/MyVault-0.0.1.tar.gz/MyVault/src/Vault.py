import configparser
import os
import shutil
import sqlite3
import sys
from datetime import datetime
from typing import NoReturn, Tuple

from MyVault.src.statics import exit_codes, messages, prompts
from MyVault.src.utils import AESEncryption, Database, clipboard, queries


class Vault(AESEncryption):
    def __init__(self, db_path: str, config_path: str):
        key, salt, iterations, clipboard_ttl = self.__get_cipher_params(
            config_path=config_path
        )
        super().__init__(key=key, salt=salt, iterations=iterations)
        self.__set_db(db_path=db_path)
        self.__config_path = config_path
        self.clipboard_ttl = clipboard_ttl

    def __enter__(self):
        return self

    @staticmethod
    def __get_cipher_params(config_path: str) -> Tuple[str, str, int, int]:
        config = configparser.ConfigParser()
        config.read(filenames=config_path, encoding="utf-8")
        try:
            return (
                config["cipher"]["key"],
                config["cipher"]["salt"],
                int(config["cipher"]["iterations"]),
                int(config["cipher"]["clipboard_ttl"]),
            )
        except KeyError:
            print(messages.CONFIG_KEY_WARNING)
            sys.exit(exit_codes.INVALID_KEY)
        except ValueError:
            print(messages.CONFIG_VALUE_WARNING)
            sys.exit(exit_codes.INVALID_VALUE)

    def __set_db(self, db_path: str) -> NoReturn:
        if os.path.exists(db_path) is False:
            create = input(prompts.CREATE_SQLITE_DB_CONFIRM)
            if create != "yes":
                print(messages.DB_REQUIRED_WARNING)
                sys.exit(0)

            os.makedirs(name=os.path.dirname(os.path.realpath(db_path)), exist_ok=True)
            print(messages.DB_CREATED.format(db_path))
        else:
            pass
        self.db = Database(db_path=db_path)
        self.__db_path = db_path

    def upsert(self, folder: str, name: str, secret: str) -> NoReturn:
        secret_encrypted = self.encrypt(plaintext=secret)
        try:
            self.db.insert_secret(folder=folder, name=name, secret=secret_encrypted)
            print(messages.SECRET_INSERTED.format(folder, name))
        except sqlite3.IntegrityError:
            update = input(prompts.UPDATE_SECRET_CONFIRM.format(folder, name))
            if update != "yes":
                print(messages.UPDATE_ABORTED)
                sys.exit(0)

            self.db.update_secret(folder=folder, name=name, new_secret=secret_encrypted)
            print(messages.SECRET_UPDATED.format(folder, name))

    def list_(self) -> NoReturn:
        print(messages.FOLDERS_NAMES_PRINT)
        for (folder, name) in self.db.select_folder_and_names():
            print(f"{folder}/{name}")

    def copy(self, folder: str, name: str, get: bool = False) -> NoReturn:
        secret_encrypted = self.db.select_secret(folder=folder, name=name)
        if secret_encrypted is None:
            print(messages.SECRET_NOT_FOUND.format(folder, name))
            sys.exit(exit_codes.SECRET_NOT_FOUND)
        else:
            try:
                secret_decrypted = self.decrypt(ciphertext=secret_encrypted)
            except UnicodeDecodeError:
                print(messages.INVALID_CONFIG_WARNING)
                sys.exit(exit_codes.INVALID_CONFIG)

            if get is True:
                return secret_encrypted
            else:
                print(messages.SECRET_COPIED.format(folder, name, self.clipboard_ttl))
                clipboard.copy(text=secret_decrypted, ttl_secs=self.clipboard_ttl)

    def update_encryption(self, new_config_path: str) -> NoReturn:
        update = input(
            prompts.ENCRYPTION_UPDATE_CONFIRM.format(
                self.__db_path, self.__config_path, new_config_path
            )
        )
        if update != "yes":
            print(messages.ENCRYPTION_ABORTED)
            sys.exit(0)

        update_params = list()
        key, salt, iterations, _ = self.__get_cipher_params(config_path=new_config_path)
        new_cipher = AESEncryption(key=key, salt=salt, iterations=iterations)
        for (folder, name, secret_encrypted) in self.db.select_all():
            time_now = datetime.now()
            secret_decrypted = self.decrypt(secret_encrypted)
            new_secret_encrypted = new_cipher.encrypt(plaintext=secret_decrypted)
            update_params.append((new_secret_encrypted, time_now, folder, name))

        backup_db_path = self.__backup_db()
        self.db.execute_many(queries.UPDATE_SECRET, update_params)
        print(messages.ENCRYPTION_UPDATED.format(backup_db_path))

    def __backup_db(self) -> str:
        path_split = self.__db_path.rsplit(".", 1)
        time_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_path = f"{path_split[0]}.backup_{time_now}.{path_split[1]}"
        shutil.copy2(self.__db_path, new_path)
        return new_path

    def remove(self, folder: str, name: str) -> NoReturn:
        remove = input(prompts.REMOVE_SECRET_CONFIRM.format(folder, name))
        if remove != "yes":
            print(messages.REMOVE_ABORTED)
            sys.exit(0)

        self.db.delete_secret(folder=folder, name=name)
        print(messages.SECRET_DELETED.format(folder, name))

    def __exit__(self, exc_type, exc_val, exc_tb) -> NoReturn:
        if isinstance(self.db, Database):
            self.db.close()
            print(messages.DB_CONN_CLOSED)
