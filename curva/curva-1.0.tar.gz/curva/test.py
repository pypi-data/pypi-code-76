from unittest import main, TestCase
from curva import Curva
from .key import ECKeys
from .aes import *
import os, random

class CurvaTestCase(TestCase):
    def setUp(self):
        self.c1 = Curva()
        self.c2 = Curva()
        self.c1.load(self.c2.export())
        self.c2.loadHex(self.c1.exportHex())
    def testSecret(self):
        self.assertEqual(self.c1.secret(), self.c2.secret(), "Shared secret unequal.")
    def testSign(self):
        data = os.urandom(64)
        signature = self.c2.sign(data)
        self.assertTrue(self.c1.verify(data, signature), 'Curva 1 signature verification failed.')
        data = os.urandom(64)
        signature = self.c1.sign(data)
        self.assertTrue(self.c2.verify(data, signature), 'Curva 2 signature verification failed.')
    def testEncrypt(self):
        data = os.urandom(64)
        encrypted = self.c1.encrypt(data)
        self.assertEqual(self.c2.decrypt(encrypted), data, '1 -> 2 encrypt / decrypt failed.')
        data = os.urandom(64)
        encrypted = self.c2.encrypt(data)
        self.assertEqual(self.c1.decrypt(encrypted), data, '2 -> 1 encrypt / decrypt failed.')

class KeyTestCase(TestCase):
    def setUp(self):
        self.k1 = ECKeys()
        self.k2 = ECKeys()
        self.k1.load(self.k2.export())
        self.k2.loadHex(self.k1.exportHex())
    def testSecret(self):
        self.assertEqual(self.k1.secret(), self.k2.secret(), "Shared secret unequal.")
    def testSign(self):
        data = os.urandom(64)
        signature = self.k2.sign(data)
        self.assertTrue(self.k1.verify(data, signature), 'Curva 1 signature verification failed.')
        data = os.urandom(64)
        signature = self.k1.sign(data)
        self.assertTrue(self.k2.verify(data, signature), 'Curva 2 signature verification failed.')

class AesTestCase(TestCase):
    def testPad(self):
        data = os.urandom(15)
        self.assertEqual(data + b'\1', pad_data(data), 'Incorrect padding.')
        data = os.urandom(16)
        self.assertEqual(data + b'\x10' * 16, pad_data(data), 'Incorrect padding.')
        data = os.urandom(random.randrange(100))
        padded = pad_data(data)
        self.assertEqual(data, unpad_data(padded), 'Incorrect unpadding.')
        self.assertRaises(InvalidPadding, unpad_data, b'ThisIsInvalid')
    def testEncrypt(self):
        key = os.urandom(32)
        data = os.urandom(64)
        self.assertEqual(data, decrypt(key, encrypt(key, data)), 'encrypt / decrypt failed.')

if __name__ == '__main__':
    main()