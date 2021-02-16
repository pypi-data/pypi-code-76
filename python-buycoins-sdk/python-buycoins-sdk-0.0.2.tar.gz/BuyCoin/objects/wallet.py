import uuid

from BuyCoin.objects.errors import ParameterNotAllowed
from BuyCoin.utils import buycoin_params


class Wallet:
    operation = None
    cryptocurrency = None
    coin_amount = None
    address = None

    def __init__(self, operation, cryptocurrency, coin_amount=None, address=None):
        cryptocurrency = cryptocurrency.lower()
        operation = operation.lower()
        if cryptocurrency not in buycoin_params["allowed_cryptocurrency"]:
            raise ParameterNotAllowed("This cryptocurrency is not supported")
        if operation not in buycoin_params["operation"]:
            raise ParameterNotAllowed("Invalid operation, options are 'buy', 'sell' ")
        if not coin_amount:
            if operation != "create" and operation != "balance":
                raise ParameterNotAllowed("Specify amount of coins to be bought")

        if operation == "send":
            if not address:
                raise ParameterNotAllowed("Specify the address to be sent to")

        if operation in ["send", "buy", "sell"]:
            if not coin_amount:
                raise ParameterNotAllowed("Specify the amount of coin as a decimal")

        self.cryptocurrency = cryptocurrency
        self.operation = operation
        self.coin_amount = coin_amount

    def generate_reference_code(self):
        """
        Return unique reference code
        """
        return uuid.uuid4
