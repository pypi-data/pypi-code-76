from .base_datatype_mapper import BaseDatatypeMapper

class ByteMapper(BaseDatatypeMapper):
    """A Mapper class for byte encoding data

    This mapper is typically used with the ByteBuffer datatype. This class will
    automatically encode the value passed for both mapping and reconstructing. So, even

    For example::

         mapper = ByteMapper(DynamoDataType(condition_type="B"))
         # You can pass a string if you wanted to for example
         mapper.map("hello world")
         {'B': b'hello world'}

         # But the string will not be returned when reconstructing
         mapper.reconstruct({'B': b'hello world'})
         b'helo world'
    """
    def resolve(self, value):
        """UTF-8 encode the value

        Parameters:
            value: a string to be encoded or an already encoded stream.

        Returns:
            a UTF-8 encoded version of value. If the value fails to be utf-8 encoded, it
            will return the value as-is
        """
        return self._encode(value)

    def parse(self, value):
        """UTF-8 encode the value

        Parameters:
            value: a string to be encoded or an already encoded stream.

        Returns:
            a UTF-8 encoded version of value. If the value fails to be utf-8 encoded, it
            will return the value as-is
        """
        return self._encode(value)

    def _encode(self, value):
        """try to encode it or return the value (meaning its already encoded"""
        try:
            return value.encode('utf-8')
        except AttributeError:
            return value
