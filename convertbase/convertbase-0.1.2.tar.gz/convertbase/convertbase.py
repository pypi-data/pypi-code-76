"""Universal base converter"""


class Convertbase:

    def __init__(self):
        """
        Sets default values to base32 and RFC4648 standard.
        """
        self.base = 32
        self.charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

    @classmethod
    def to_b32(cls, n: int, base: int =32):
        """ Using The RFC 4648 Base 32 charset"""
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
        if n < base:
            return charset[n]
        else:
            floor = n // base
            remainder = n % base
            return cls.to_b32(floor, base) + charset[remainder]

    @classmethod
    def to_hex(cls, n: int, base: int =16):
        charset = "0123456789abcdef"
        if n < base:
            return charset[n]
        else:
            floor = n // base
            remainder = n % base
            return cls.to_hex(floor, base) + charset[remainder]

    @classmethod
    def from_b32_to_dec(cls, n, base=32):
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
        result = 0
        for i, char in enumerate(reversed(n)):
            result = result + (charset.index(char) * 32**i)
        return result

    def set_base(self, base: int) -> None:
        """
        If user wants to set base: int
        """
        self.base = base

    def set_charset(self, charset: str) -> None:
        """
        Use to set custom charset. Default is RFC4648.
        """
        self.charset = charset

    def convert(self, n: int) -> str:
        """
        Convert to self.base, using self.charset.
        Default is using base32 and RFC4648.
        """
        if n < self.base:
            return self.charset[n]
        else:
            floor = n // self.base
            remainder = n % self.base
            return self.convert(floor) + self.charset[remainder]
