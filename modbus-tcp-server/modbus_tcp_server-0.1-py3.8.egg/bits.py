class BitStream:
    def __init__(self):
        self.pointer = 0
        self.data = bytearray()

    def __len__(self):
        return len(self.data)

    def __bytes__(self):
        return bytes(self.data)

    def add(self, bit: bool):
        ptr = self.pointer % 8
        value = 1 << ptr if bit else 0
        if not ptr:
            self.data += b'\x00'
        self.data[-1] = self.data[-1] | value
        self.pointer += 1

