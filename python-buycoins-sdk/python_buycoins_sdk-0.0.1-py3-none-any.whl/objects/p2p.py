from BuyCoin.objects.errors import ParameterNotAllowed
from BuyCoin.utils import buycoin_params


class P2P:
    """
    """
    operations = ["pmo", "plo"]
    price_types = ["static", "dynamic"]

    operation = None
    cryptocurrency = None
    coinAmount = None
    staticPrice = None
    priceType = None
    dynamicExchangeRate = None
    orderSide = None

    def __init__(self, side, coin_amount, cryptocurrency, operation, price_type=None,
                 static_price=None, dynamic_exchange_rate=None):
        if operation not in self.operations:
            raise ParameterNotAllowed("Please specify the operation to be done. 'pmo' refers to 'Place Market Order'\
                (place order at market price).\
                'plo' refers to 'Place Limit Order' \
                (requires a specific price type and its rate)")
        if operation == "plo":
            if price_type not in self.price_types:
                raise ParameterNotAllowed(
                    f"Price type cannot be {price_type}. Price type is either 'dynamic' or 'static'")
            else:
                if price_type == "static" and not static_price:
                    raise ParameterNotAllowed("Please specify a static price")
                if price_type == "dynamic" and not dynamic_exchange_rate:
                    raise ParameterNotAllowed("Please specify a dynamic exchange rate")

                self.dynamicExchangeRate = dynamic_exchange_rate
                self.staticPrice = static_price
                self.priceType = price_type

        if cryptocurrency not in buycoin_params["allowed_cryptocurrency"]:
            raise ParameterNotAllowed("This cryptocurrency is not supported")

        if side not in buycoin_params["side"]:
            raise ParameterNotAllowed(f"This {side} is not supported, only 'buy' and 'sell'")

        self.operation = operation
        self.cryptocurrency = cryptocurrency
        self.coinAmount = coin_amount
        self.orderSide = side
