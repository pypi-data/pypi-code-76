from pyalgo.basic_modules import default_functions, default_values
from . import compiled_functions


class XOR_Cipher:
    def __init__(self, key, description: str = ""):
        self.check_if_key_is_valid(key)

        self.key = key

        self.description = description

    def encrypt_bytes(self, bytes, key=None):
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if not (isinstance(bytes, ByteType) or isinstance(bytes, ByteArrayType)):
            raise TypeError("'bytes' needs to be byte type or bytearray type")

        if key == None:
            key = self.key
        else:
            self.check_if_key_is_valid(key)

        if isinstance(bytes, ByteType):
            bytes = bytearray(bytes)

        for i, value in enumerate(bytes):
            if isinstance(key, default_values.IntType):
                bytes[i] = key ^ value
            else:
                bytes[i] = key[i % len(key)] ^ value

        return bytes

    def decrypt_bytes(self, bytes, key=None):
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if not (isinstance(bytes, ByteType) or isinstance(bytes, ByteArrayType)):
            raise TypeError("'bytes' needs to be byte type or bytearray type")

        if key == None:
            key = self.key
        else:
            self.check_if_key_is_valid(key)

        if isinstance(bytes, ByteType):
            bytes = bytearray(bytes)

        for i, value in enumerate(bytes):
            if isinstance(key, default_values.IntType):
                bytes[i] = key ^ value
            else:
                bytes[i] = key[i % len(key)] ^ value

        return bytes

    def encrypt_file(self, path, key: int = None, include_additional_end: bool = True, additional_end="enc"):
        if key == None:
            key = self.key
        else:
            self.check_if_key_is_valid(key)

        with open(path, "br") as file:
            bytes = file.read()

        bytes = self.encrypt_bytes(bytes, key)

        if include_additional_end:
            path += additional_end

        with open(path, "bw") as file:
            file.write(bytes)

        print("the file has encrypted properly")

    def decrypt_file(self, path, key=None, remove_additional_end: bool = True, additional_end="enc"):
        if key == None:
            key = self.key
        else:
            self.check_if_key_is_valid(key)

        with open(path, "br") as file:
            bytes = file.read()

        bytes = self.decrypt_bytes(bytes, key)

        if remove_additional_end:
            path = path[:-len(additional_end)]

        with open(path, "bw") as file:
            file.write(bytes)

        print("the file has decrypted properly")

    @staticmethod
    def check_if_key_is_valid(key):
        IntType, ListType = default_values.IntType, default_values.ListType

        if not (isinstance(key, IntType) or isinstance(key, ListType)):
            raise TypeError("'key' can be an int type or a list type")

        if isinstance(key, IntType):
            if key >= 256:
                raise ValueError("'key' cannot be bigger than 255")

            if key < 0:
                raise ValueError("'key' cannot be smaller than 0")
        elif isinstance(key, ListType):
            for i in key:
                if i >= 256:
                    raise ValueError("any number in 'key' cannot be bigger than 255")

                if i < 0:
                    raise ValueError("any number in 'key' cannot be smaller than 0")


class RSA():
    def __init__(self, p, q, e, description: str):
        self.p = p
        self.q = q
        self.e = e

        self.Phi = ((self.p - 1) * (self.q - 1))

        self.description = description

        if e >= self.Phi:  raise ValueError(f"'e' cannot be bigger that phi({self.Phi})")

        self.check_if_e_is_valid(e, p, q)
        if default_functions.prime_check(e) == False:  raise ValueError("'e' should be prime")
        if default_functions.prime_check(p) == False:  raise ValueError("'p' should be prime")
        if default_functions.prime_check(q) == False:  raise ValueError("'q' should be prime")

        self.N = p * q  # compute N

    def check_if_e_is_valid(self, e=None, p=None, q=None):

        if e == None:  e == self.e
        if p == None:  p == self.p
        if q == None:  q == self.q
        if not (default_functions.gcd(e, self.Phi) == 1):
            raise ValueError("'e' should not have a gcd with φ(p, q) that is not 1")

    def find_private_key(self):
        self.d = compiled_functions.find_private_key(self.e, self.Phi)

    def encrypt(self, M, N=None, e=None):

        StringType = default_values.StringType

        if N == None:  N = self.N
        if e == None:  e = self.e

        if not isinstance(M, StringType):  raise TypeError("'M' should be a string")

        M = [ord(char) for char in M]  # transfer into bytes

        # return [((value ** e) % N) for value in M]
        return [pow(value, e, N) for value in M]

    def decrypt(self, C, N=None, d=None):
        ListType = default_values.ListType

        if N == None:  N = self.N
        if d == None:  d = self.d

        if not isinstance(C, ListType):  raise TypeError("'C' should be a List")

        M = ""
        powered = 1

        for idx, value in enumerate(C):
            M += chr(pow(value, d, N))
            print(f"Iteration {idx + 1} \\ {len(C)}")

        return M

    @property
    def private_key(self):
        return {"d": self.d, "e": self.e}

    @property
    def public_key(self):
        return {"N": self.N, "e": self.e}

    @property
    def key(self):
        return {"N": self.N, "d": self.d, "e": self.e}

    def save_key_to_dir(self, key_to_save=None, dir=None, filename="key.rsa"):
        dictionaryType = default_values.DictionatyType
        if (not (key_to_save == None)):
            if not isinstance(key_to_save, dictionaryType):
                print("'key_to_save' needs to be a dictionary type")
        else:
            key_to_save = self.key

        dir += "\\" + str(filename)

        content = ""
        for i in key_to_save:
            content += "{} {} \n".format(i, self.key[i])

        file = open(dir, "w")
        file.write(content)
        file.close()

        print("saved")

    def save_public_key_to_dir(self, dir=None, filename="public_key.rsa"):

        dir += "\\" + str(filename)

        content = ""
        for i in self.public_key:
            content += "{} {} \n".format(i, self.key[i])

        file = open(dir, "w")
        file.write(content)
        file.close()

        print("saved")

    def save_private_key_to_dir(self, dir=None, filename="private_key.rsa"):

        dir += "\\" + str(filename)

        content = ""
        for i in self.private_key:
            content += "{} {} \n".format(i, self.key[i])

        file = open(dir, "w")
        file.write(content)
        file.close()

        print("saved")

    def load_keys(self, dir):
        with open(dir) as file:
            content = file.readlines()

        for i in content:
            if i[0] == "e":
                self.e = int(i[2:-2])
            if i[0] == "d":
                self.d = int(i[2:-2])
            if i[0] == "N":
                self.N = int(i[2:-2])

        print("loaded")

    def clear_keys(self):
        del self.e
        del self.d
        del self.N

    def print_public_key(self):
        print(f"N = {self.N}")
        print(f"e = {self.e}")

    def print_private_key(self):
        print(f"N = {self.N}")
        print(f"d = {self.d}")

    def print_key(self):
        print(f"N = {self.N}")
        print(f"e = {self.e}")
        print(f"d = {self.d}")