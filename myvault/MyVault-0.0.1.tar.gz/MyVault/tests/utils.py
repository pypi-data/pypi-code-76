import unittest

from MyVault.src.utils import AESEncryption


class TestUtils(unittest.TestCase):

    PASSWORD = "password"

    KEY = "key_correct"
    SALT = "salt_correct"
    ITER = 10000

    CIPHER = AESEncryption(key=KEY, salt=SALT, iterations=ITER)

    KEY_BAD = "key_incorrect"
    SALT_BAD = "salt_incorrect"
    ITER_BAD = ITER // 2

    def get_encrypted_password(self) -> str:
        return self.CIPHER.encrypt(plaintext=self.PASSWORD)

    def test_01_check_encryption(self):
        pwd_enc_1 = self.get_encrypted_password()
        pwd_enc_2 = self.get_encrypted_password()
        self.assertNotEqual(pwd_enc_1, pwd_enc_2)

        pwd_dec_1 = self.CIPHER.decrypt(ciphertext=pwd_enc_1)
        pwd_dec_2 = self.CIPHER.decrypt(ciphertext=pwd_enc_2)
        self.assertEqual(pwd_dec_1, pwd_dec_2)
        self.assertEqual(pwd_dec_1, self.PASSWORD)

    def test_02_check_encryption_bad_key(self):
        pwd_enc = self.get_encrypted_password()
        cipher = AESEncryption(key=self.KEY_BAD, salt=self.SALT, iterations=self.ITER)
        pwd_dec_bad_key = cipher.decrypt(ciphertext=pwd_enc)
        self.assertNotEqual(pwd_dec_bad_key, self.PASSWORD)

    def test_03_check_encryption_bad_salt(self):
        pwd_enc = self.get_encrypted_password()
        cipher = AESEncryption(key=self.KEY, salt=self.SALT_BAD, iterations=self.ITER)
        pwd_dec_bad_salt = cipher.decrypt(ciphertext=pwd_enc)
        self.assertNotEqual(pwd_dec_bad_salt, self.PASSWORD)

    def test_04_check_encryption_bad_iterations(self):
        pwd_enc = self.get_encrypted_password()
        cipher = AESEncryption(key=self.KEY, salt=self.SALT_BAD, iterations=self.ITER)
        pwd_dec_bad_iter = cipher.decrypt(ciphertext=pwd_enc)
        self.assertNotEqual(pwd_dec_bad_iter, self.PASSWORD)


if __name__ == "__main__":
    unittest.main()
