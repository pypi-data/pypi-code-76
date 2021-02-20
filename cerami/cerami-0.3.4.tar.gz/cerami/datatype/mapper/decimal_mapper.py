from decimal import Decimal
from .base_datatype_mapper import BaseDatatypeMapper

class DecimalMapper(BaseDatatypeMapper):
    """A Mapper class for converting decimal number fields into DynaomDB dictionaries

    For example::

        mapper = DecimalMapper(Number())
        mapper.map(30)
        {'N': '30'}

        mapper.map(30.69213)
        {'N': '30.69213'}

        mapper.reconstruct({'N': '30'})
        Decimal('30')

        mapper.reconstruct({'N': '30.69213'})
        Decimal('30.69213')
    """
    def resolve(self, value):
        """convert the number into a decimal string"""
        return str(Decimal(str(value)))

    def parse(self, value):
        """convert the value back into a Decimal"""
        return Decimal(value)
