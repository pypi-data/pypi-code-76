# -*- coding: utf-8 -*-

import ctypes
import os
import platform

class AsymmetricAlgo(object):

    asymmetric_lib = None
    is_python3 = False

    def __init__(self, likes_spam=False):
        """Inits AsymmetricAlgo ."""

        py_version = platform.architecture()
        if py_version[0] != "32bit":
            raise Exception("64-bit python is not supported")

        oldcwd = os.getcwd()

        path = os.path.split(os.path.realpath(__file__))[0]

        lib_path_test = os.path.join(oldcwd, "asymmetric_algo.dll")

        lib_path_select = ""

        from quick_data_clean.quick_file import File

        if File.is_file_exists(lib_path_test):
            lib_path_select = lib_path_test
        else:
            lib_path_select = os.path.join(path, "asymmetric_algo.dll")

        # print(lib_path_select)

        self.asymmetric_lib = ctypes.cdll.LoadLibrary(lib_path_select)

        '''
        try:
            # os.chdir(path)
            self.asymmetric_lib = ctypes.cdll.LoadLibrary(lib_path_select)

        finally:

            os.chdir(oldcwd)
        '''

        py_version = platform.python_version()
        self.is_python3 = False
        if py_version[0] == "3":
            self.is_python3 = True


class SM2(object):

    def __init__(self):
        AsymmetricAlgo.__init__(self)

        self.x = ""
        self.y = ""
        self.d = ""

    def __str__(self):
        return "x:{} y:{} d:{}".format(self.x, self.y, self.d)

    def set_public_key(self, x, y):

        if len(x) != 64:
            raise Exception("the legth of x[parameter] must be 64[32 bytes]")

        if len(y) != 64:
            raise Exception("the legth of y[parameter] must be 64[32 bytes]")

        self.x = x
        self.y = y

    def set_private_key(self, d):

        if len(d) != 64:
            raise Exception("the legth of d[parameter] must be 64[32 bytes]")

        self.d = d

    def generate_key(self):
        self.x = "R" * 200
        self.y = "R" * 200
        self.d = "R" * 200

        if self.is_python3:
            self.x = bytes(self.x, "utf-8")
            self.y = bytes(self.y, "utf-8")
            self.d = bytes(self.d, "utf-8")

        result = self.asymmetric_lib.SM2KeyGenerator(self.d, self.x, self.y)
        if result != 0:
            raise Exception("failed to generate key of sm2")

        if self.is_python3:
            self.x = self.x.decode()
            self.y = self.y.decode()
            self.d = self.d.decode()

        self.x = self.x.replace("R", "")
        self.y = self.y.replace("R", "")
        self.d = self.d.replace("R", "")

    def sign(self, msg):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        s = "R" * 200
        r = "R" * 200

        if self.is_python3:
            self.x = bytes(self.x, "utf-8")
            self.y = bytes(self.y, "utf-8")
            self.d = bytes(self.d, "utf-8")
            msg = bytes(msg, "utf-8")
            s = bytes(s, "utf-8")
            r = bytes(r, "utf-8")

        result = self.asymmetric_lib.SM2Sign(self.d, self.x, self.y, msg, s, r)
        if result != 0:
            raise Exception("failed to sign")

        if self.is_python3:
            s = s.decode()
            r = r.decode()
            self.x = self.x.decode()
            self.y = self.y.decode()
            self.d = self.d.decode()

        return s.replace("R", "") + r.replace("R", "")

    def verify(self, msg, sign_s_r):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        if len(sign_s_r) != 128:
            raise Exception("the legth of sign_s_r[parameter] must be 128[64 bytes]")

        s = sign_s_r[0:64]
        r = sign_s_r[64:128]
        # print("s:",s,"r:",r)

        if self.is_python3:
            self.x = bytes(self.x, "utf-8")
            self.y = bytes(self.y, "utf-8")
            msg = bytes(msg, "utf-8")
            s = bytes(s, "utf-8")
            r = bytes(r, "utf-8")

        result = self.asymmetric_lib.SM2Verify(self.x, self.y, msg, s, r)
        if self.is_python3:
            self.x = self.x.decode()
            self.y = self.y.decode()

        if result == 0:
            return True
        else:
            return False

    def encrypt(self, msg):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        result_data = "R" * (len(msg) + 196)

        if self.is_python3:
            self.x = bytes(self.x, "utf-8")
            self.y = bytes(self.y, "utf-8")
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        result = self.asymmetric_lib.SM2Enctypt(self.x, self.y, msg, result_data)
        if self.is_python3:
            self.x = self.x.decode()
            self.y = self.y.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")

    def decrypt(self, msg):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        result_data = "R" * (len(msg) + 196)

        if self.is_python3:
            self.d = bytes(self.d, "utf-8")
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        result = self.asymmetric_lib.SM2Decrypt(self.d, msg, result_data)

        if self.is_python3:
            self.d = self.d.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")


class SM3(object):

    def __init__(self):
        AsymmetricAlgo.__init__(self)

    def get_hash(self, msg):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        result_data = "R" * 100
        if self.is_python3:
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        result = self.asymmetric_lib.SM3Hash(msg, result_data)

        if self.is_python3:
            msg = msg.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")


class RSA(object):

    def __init__(self):
        AsymmetricAlgo.__init__(self)

        self.bits = 0
        self.e = ""
        self.n = ""
        self.d = ""
        self.p = ""
        self.q = ""
        self.dp = ""
        self.dq = ""
        self.qinv = ""
        self.set_private_key_type = 0

    def __str__(self):
        return "bits:{} e:{} n:{} d:{} p:{} q:{} dp:{} dq:{} qinv:{}".format(self.bits,
                self.e, self.n, self.d, self.p, self.q, self.dp, self.dq, self.qinv)

    def set_public_key(self, e, n):

        if e != "03" and e != "10001":
            raise Exception("the value of e[parameter] must be \"03\" or \"10001\"  ")

        if len(n) % 2 != 0:
            raise Exception("the legth of n[parameter] must be a even "
                            "number")

        self.e = e
        self.n = n
        self.bits = int(len(n) / 2 * 8)

    def set_private_key(self, e, *args):

        if e != "03" and e != "10001":
            raise Exception("the value of e[parameter] must be \"03\" or \"10001\"  ")

        if len(args) != 1 and len(args) != 5:
            raise Exception("Either there is only one parameter(d) or five parameters(p,q,dp,dq,qinv) after the parameter e")

        self.e = e

        if len(args) == 1:
            self.d = args[0]
            self.set_private_key_type = 2
            self.bits = int(len(args[0]) / 2 * 8)
        else:
            self.p = args[0]
            self.q = args[1]
            self.dp = args[2]
            self.dq = args[3]
            self.qinv = args[4]
            self.set_private_key_type = 3
            self.bits = int(len(args[0]) * 8)

    def generate_key(self, bits, e):

        if e != "03" and e != "10001":
            raise Exception("the value of e[parameter] must be \"03\" or \"10001\"  ")

        self.bits = bits
        self.e = e

        padding_length = int(self.bits / 8) + 1
        self.n = "R" * padding_length * 2
        self.d = "R" * padding_length * 2
        self.p = "R" * padding_length
        self.q = "R" * padding_length
        self.dp = "R" * padding_length
        self.dq = "R" * padding_length
        self.qinv = "R" * padding_length

        if self.is_python3:
            self.e = bytes(self.e, "utf-8")
            self.n = bytes(self.n, "utf-8")
            self.d = bytes(self.d, "utf-8")
            self.p = bytes(self.p, "utf-8")
            self.q = bytes(self.q, "utf-8")
            self.dp = bytes(self.dp, "utf-8")
            self.dq = bytes(self.dq, "utf-8")
            self.qinv = bytes(self.qinv, "utf-8")

        result = self.asymmetric_lib.RSAKeyGenerator(self.bits, self.e, self.n, self.d,
                                                     self.p, self.q, self.dp, self.dq, self.qinv)
        if result != 0:
            raise Exception("failed to generate key of rsa")

        if self.is_python3:
            self.e = self.e.decode()
            self.n = self.n.decode()
            self.d = self.d.decode()
            self.p = self.p.decode()
            self.q = self.q.decode()
            self.dp = self.dp.decode()
            self.dq = self.dq.decode()
            self.qinv = self.qinv.decode()

        self.n = self.n.replace("R", "")
        self.d = self.d.replace("R", "")
        self.p = self.p.replace("R", "")
        self.q = self.q.replace("R", "")
        self.dp = self.dp.replace("R", "")
        self.dq = self.dq.replace("R", "")
        self.qinv = self.qinv.replace("R", "")

        self.set_private_key_type = 1

    def encrypt_pri(self, msg, padding=3):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        if padding != 3 and padding != 1:
            raise Exception("the value of padding[parameter] must be 3 or 1 ")

        if padding == 3:
            msg_len = int(len(msg) /2)
            if msg_len % int(len(self.n)/2) != 0:
                raise Exception("use mode RSA_NO_PADDING.The input data must be an integer multiple of the key length")

        else:
            msg_len = int(len(msg) /2)
            if msg_len >  (int(len(self.n)/2) - 11):
                raise Exception("use mode RSA_PKCS1_PADDING.The input data cannot be greater than the key length minus 11 bytes")

        result_data = "R" * int(len(self.n))

        if self.is_python3:
            self.e = bytes(self.e, "utf-8")
            self.n = bytes(self.n, "utf-8")
            self.d = bytes(self.d, "utf-8")
            self.p = bytes(self.p, "utf-8")
            self.q = bytes(self.q, "utf-8")
            self.dp = bytes(self.dp, "utf-8")
            self.dq = bytes(self.dq, "utf-8")
            self.qinv = bytes(self.qinv, "utf-8")
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        result = -1

        if self.set_private_key_type <= 2:
            result = self.asymmetric_lib.RSASign(self.e, self.n, self.d, msg,
                                                 result_data, padding)
        else:
            # char *exponent,char *n,char *p,
            # char *q,char *dp,char *dq,char *qinv,char *msg,
            # char *result,int padding=3

            result = self.asymmetric_lib.RSASign2(self.e, self.n, self.p,
                                                  self.q, self.dp, self.dq,
                                                  self.qinv, msg,
                                                  result_data, padding)

        if result != 0:
            raise Exception("failed to encrypt")

        if self.is_python3:
            self.e = self.e.decode()
            self.n = self.n.decode()
            self.d = self.d.decode()
            self.p = self.p.decode()
            self.q = self.q.decode()
            self.dp = self.dp.decode()
            self.dq = self.dq.decode()
            self.qinv = self.qinv.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")

    def decrypt_pub(self, msg, padding=3):
        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        if padding != 3 and padding != 1:
            raise Exception("the value of padding[parameter] must be 3 or 1 ")

        msg_len = int(len(msg)/2)

        result_data = "R" * msg_len * 2

        if self.is_python3:
            self.e = bytes(self.e, "utf-8")
            self.n = bytes(self.n, "utf-8")
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        # char *exponent,char *n,char *msg, char *result,int padding=3
        result = self.asymmetric_lib.RSAVerify(self.e, self.n, msg, result_data, padding)
        if result != 0:
            raise Exception("failed to decrypt")

        if self.is_python3:
            self.e = self.e.decode()
            self.n = self.n.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")

    def encrypt_pub(self, msg, padding=3):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        if padding != 3 and padding != 1:
            raise Exception("the value of padding[parameter] must be 3 or 1 ")

        if padding == 3:
            msg_len = int(len(msg) /2)
            if msg_len % int(len(self.n)/2) != 0:
                raise Exception("use mode RSA_NO_PADDING.The input data must be an integer multiple of the key length")

        else:
            msg_len = int(len(msg) /2)
            if msg_len >  (int(len(self.n)/2) - 11):
                raise Exception("use mode RSA_PKCS1_PADDING.The input data cannot be greater than the key length minus 11 bytes")

        result_data = "R" * int(len(self.n))
        
        if self.is_python3:
            self.e = bytes(self.e, "utf-8")
            self.n = bytes(self.n, "utf-8")
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        # char *exponent,char *n,char *msg, char *result,int padding=3
        result = self.asymmetric_lib.RSAEnctypt(self.e, self.n, msg, result_data, padding)
        if result != 0:
            raise Exception("failed to encrypt")

        if self.is_python3:
            self.e = self.e.decode()
            self.n = self.n.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")

    def decrypt_pri(self, msg, padding=3):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        if padding != 3 and padding != 1:
            raise Exception("the value of padding[parameter] must be 3 or 1 ")

        msg_len = int(len(msg) / 2)

        result_data = "R" * msg_len * 2

        if self.is_python3:
            self.e = bytes(self.e, "utf-8")
            self.n = bytes(self.n, "utf-8")
            self.d = bytes(self.d, "utf-8")
            self.p = bytes(self.p, "utf-8")
            self.q = bytes(self.q, "utf-8")
            self.dp = bytes(self.dp, "utf-8")
            self.dq = bytes(self.dq, "utf-8")
            self.qinv = bytes(self.qinv, "utf-8")
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        result = -1

        if self.set_private_key_type <= 2:
            result = self.asymmetric_lib.RSADecrypt(self.e, self.n, self.d, msg,
                                                 result_data, padding)
        else:
            # char *exponent,char *n,char *p,
            # char *q,char *dp,char *dq,char *qinv,char *msg,
            # char *result,int padding=3

            result = self.asymmetric_lib.RSADecrypt2(self.e, self.n, self.p,
                                                  self.q, self.dp, self.dq,
                                                  self.qinv, msg,
                                                  result_data, padding)

        if result != 0:
            raise Exception("failed to decrypt")

        if self.is_python3:
            self.e = self.e.decode()
            self.n = self.n.decode()
            self.d = self.d.decode()
            self.p = self.p.decode()
            self.q = self.q.decode()
            self.dp = self.dp.decode()
            self.dq = self.dq.decode()
            self.qinv = self.qinv.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")

    def sha(self, msg):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        result_data = "R" * 100
        if self.is_python3:
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        self.asymmetric_lib.sha_jay(msg, result_data)

        if self.is_python3:
            msg = msg.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")

    def sha1(self, msg):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        result_data = "R" * 100
        if self.is_python3:
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        self.asymmetric_lib.sha1_jay(msg, result_data)

        if self.is_python3:
            msg = msg.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")

    def sha256(self, msg):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        result_data = "R" * 100
        if self.is_python3:
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        self.asymmetric_lib.sha256_jay(msg, result_data)

        if self.is_python3:
            msg = msg.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")

    def sha512(self, msg):

        if len(msg) % 2 != 0:
            raise Exception("the legth of msg[parameter] must be a even "
                            "number")

        result_data = "R" * 200
        if self.is_python3:
            msg = bytes(msg, "utf-8")
            result_data = bytes(result_data, "utf-8")

        self.asymmetric_lib.sha512_jay(msg, result_data)

        if self.is_python3:
            msg = msg.decode()
            result_data = result_data.decode()

        return result_data.replace("R", "")

    def sign(self, msg, hash_method = "SHA-1"):
        import rsa 
        from quick_data_clean.quick_algo import DataAlgo
        e = int(self.e, 16)
        n = int(self.n, 16)
        d = int(self.d, 16)
        p = int(self.p, 16)
        q = int(self.q, 16)

        pri_key = rsa.PrivateKey(n, e, d, p, q)

        m = rsa.sign(DataAlgo.pack(msg),pri_key, hash_method)
        # return m.hex()
        return DataAlgo.un_pack(m)

    def verify(self, msg, sign):
        import rsa 
        from quick_data_clean.quick_algo import DataAlgo
        e = int(self.e, 16)
        n = int(self.n, 16)

        pub_key = rsa.PublicKey(e=e, n=n)

        try:
            method = rsa.verify(DataAlgo.pack(msg),DataAlgo.pack(sign),pub_key)
        except rsa.pkcs1.VerificationError as e:
            # raise
            return False
        return True

    def save_pri(self, filename):
        import rsa 
        
        e = int(self.e, 16)
        n = int(self.n, 16)
        d = int(self.d, 16)
        p = int(self.p, 16)
        q = int(self.q, 16)

        pri_key = rsa.PrivateKey(n, e, d, p, q)
        with open(filename,'w+') as f:
            f.write(pri_key.save_pkcs1().decode())

    def load_pri(self, filename):
        import rsa

        with open(filename,'r') as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

        self.n = str(hex(privkey["n"])).upper().replace("0X","")
        self.d = str(hex(privkey["d"])).upper().replace("0X","")
        self.p = str(hex(privkey["p"])).upper().replace("0X","")
        self.q = str(hex(privkey["q"])).upper().replace("0X","")
        self.e = str(hex(privkey["e"])).upper().replace("0X","")

        if self.e == "3":
            self.e = "03"
        else:
            self.e = "10001"


        self.bits = len(self.n) / 2 * 8

        self.set_private_key_type = 1

    def save_pub(self, filename):
        import rsa 

        e = int(self.e, 16)
        n = int(self.n, 16)

        pub_key = rsa.PublicKey(e=e, n=n)

        with open(filename,'w+') as f:
            f.write(pub_key.save_pkcs1().decode())

    def load_pub(self, filename):
        import rsa

        with open(filename,'r') as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

        self.n = str(hex(pubkey["n"])).upper().replace("0X","")
        self.e = str(hex(pubkey["e"])).upper().replace("0X","")

        if self.e == "3":
            self.e = "03"
        else:
            self.e = "10001"

        self.bits = len(self.n) / 2 * 8


if __name__ == '__main__':

    sm2 = SM2()

    # 生成sm2密钥
    sm2.generate_key()
    print(sm2)

    # 签名
    sign_msg = sm2.sign("12")

    # 验签
    print(sm2.verify("12",sign_msg))
    print(sm2.verify("21",sign_msg))

    sm2_1 = SM2()

    # 设置sm2密钥
    sm2_1.set_private_key("4B5A52F786BE8773640918BC9CF24195E4DC433242A9E3A1669CEE0DCF15B4B8")
    sm2_1.set_public_key("D226A1706C8E82ABB871A204ACFD433CAB206E566EAFF2991F12992682CE1400","6B3E2D1307B5EEC21BCAE4B11FDF1D11C4E2CBAD18F15447AAD02321BD817047")

    # 验签
    sign_msg = "FE762C075F57D034F75489A5F93073DE0CF55510E241FAF93B0312DBDF467D7C33E378A6F33CDB2C16D2BDA90CB2C3F302477F933CD0ADBDCE600C3F82D2E3E6"
    print(sm2_1.verify("12",sign_msg))


