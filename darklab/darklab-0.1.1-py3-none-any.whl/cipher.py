class Cipher:
    @staticmethod
    def string_to_decimal_byte_cipher(message: str):
        """
        Cipher created by DarkCeptor44
        :return:
        """

        output = []
        for ch in message:
            output.append(str(ord(ch)))
        return ' '.join(output).strip()

    @staticmethod
    def decimal_byte_cipher_to_string(message: str):
        output = []
        for ch in message.split(' '):
            output.append(chr(int(ch)))
        return ''.join(output).strip()
