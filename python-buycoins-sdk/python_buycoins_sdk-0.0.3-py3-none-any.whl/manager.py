from python_graphql_client import GraphqlClient
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError, ConnectionError
import json
import jsonpickle


from .config import BuyCoinConfig
from BuyCoin.objects.errors import QueryError, ParameterNotAllowed


class Manager:
    """
    Abstract Base Class
    """
    BUYCOIN_URL = None
    USERNAME = None
    PASSWORD = None

    def __init__(self):
        super().__init__()
        if type(self) is Manager:
            raise TypeError("Can not make instance of abstract base class")

        if not BuyCoinConfig.BUYCOIN_SECRET_KEY or not BuyCoinConfig.BUYCOIN_PUBLIC_KEY:
            raise ValueError("No secret key or public key found, \
                             assign values using BuyCoinConfig.BUYCOIN_PUBLIC_KEY = SECRET_KEY and \
                             BuyCoinConfig.BUYCOIN_PUBLIC_KEY = PUBLIC_KEY")

        self.USERNAME = BuyCoinConfig.BUYCOIN_PUBLIC_KEY
        self.PASSWORD = BuyCoinConfig.BUYCOIN_SECRET_KEY
        self.BUYCOIN_URL = BuyCoinConfig.BUYCOIN_URL

    def _create_request_args(self):
        """
        Returns required headers
        """
        auth = HTTPBasicAuth(self.USERNAME, self.PASSWORD)

        return auth

    def to_json(self, data):
        '''
        Method to serialize class instance
        '''
        data = json.JSONDecoder().decode(jsonpickle.encode(data))
        data.pop("py/object")
        return data

    def _initialize_client(self):
        """
        Create GraphQL client for executing queries
        Returns client
        """
        auth = self._create_request_args()

        try:
            _client = GraphqlClient(endpoint=self.BUYCOIN_URL, auth=auth)
        except (HTTPError, ConnectionError) as e:
            return e
        else:
            return _client

    def _perform_request(self, query, variables={}):
        self._client = self._initialize_client()
        if not query:
            return QueryError('Invalid Query')
        try:
            request = self._client.execute(query=query, variables=variables)
        except (ConnectionError, HTTPError) as e:
            raise e
        except QueryError as e:
            return e.response
        else:
            return request


class CustomerWalletManager(Manager):
    """
    Manager handles every transaction concerning cryptocurrency
    Includes buying, selling, getting prices, creating addresses and getting crypto-balance

    """
    _BUY_QUERY = """
        mutation BuyCoin($price: ID!, $coin_amount: BigDecimal!, $cryptocurrency: Cryptocurrency){
                buy(price: $price, coin_amount: $coin_amount, cryptocurrency: $cryptocurrency) {
                    id
                    cryptocurrency
                    status
                    totalCoinAmount
                    side
                }
            }
        """
    _SELL_QUERY = """
        mutation SellCoin($price: ID!, $coin_amount: BigDecimal!, $currency: Cryptocurrency){
            sell(price: $price, coin_amount: $coin_amount, cryptocurrency: $currency) {
                id
                cryptocurrency
                status
                totalCoinAmount
                side
            }
        }

    """

    _GET_PRICE_QUERY = """
        query {
            getPrices {
                id
                cryptocurrency
                buyPricePerCoin
                minBuy
                maxBuy
                expiresAt
            }
        }
        """
    _GET_CRYPTO_PRICE_QUERY = """
        query GetBuyCoinsPrices($cryptocurrency: Cryptocurrency, $side:OrderSide) {
            getPrices(cryptocurrency: $cryptocurrency, side:$side){
                buyPricePerCoin
                cryptocurrency
                id
                maxBuy
                maxSell
                minBuy
                minCoinAmount
                minSell
                sellPricePerCoin
                status
            }
        }
    """

    _CREATE_ADDRESS_QUERY = """
        mutation CreateWalletAddress($cryptocurrency: Cryptocurrency) {
            createAddress(cryptocurrency: $cryptocurrency) {
                cryptocurrency
                address
            }
        }
    """

    _SEND_CRYPTO_QUERY = """
        mutation SendCrypto($cryptocurrency: Cryptocurrency, $address: String!, $amount: BigDecimal!){
            send(cryptocurrency: $cryptocurrency, amount: $amount, address: $address) {
                id
                address
                amount
                cryptocurrency
                fee
                status
                transaction {
                    txhash
                    id
                }
            }
        }
    """
    _BALANCE_QUERY = """
        query {
            getBalances {
                id
                cryptocurrency
                confirmedBalance
            }
        }
    """

    def __init__(self):
        super().__init__()

    def get_prices(self, cryptocurrency=None, side=None):
        """
        Retrieve all cryptocurrencies current price

        Args:
            cryptocurrency: Retrieve specific cryptocurrency price

        Returns:
            response: a list of cryptocurrency and their prices
        """
        if cryptocurrency:
            if not side:
                raise ParameterNotAllowed("Please specify side, either a 'buy' or 'sell' side", status=400)

            query = self._GET_CRYPTO_PRICE_QUERY
            variables = {
                "cryptocurrency": cryptocurrency,
                "side": side
            }
        else:
            query = self._GET_PRICE_QUERY
            variables = {}

        try:
            response = self._perform_request(query=query, variables=variables)
        except Exception as e:
            raise e
        else:
            return response["data"]["getPrices"]

    def initialize_transaction(self, wallet_transaction):
        data = self.to_json(wallet_transaction)
        operation = data.pop("operation")
        variables = {**data}

        if operation == "buy":
            query = self._BUY_QUERY
            price = self.get_prices(cryptocurrency=data["cryptocurrency"], side=operation)
            variables = {**variables, "price": price[0]["id"]}
        elif operation == "sell":
            query = self._SELL_QUERY
            price = self.get_prices(cryptocurrency=data["cryptocurrency"], side=operation)
            variables = {**variables, "price": price[0]["id"]}
        elif operation == "create":
            query = self._CREATE_ADDRESS_QUERY
        elif operation == "balance":
            query = self._BALANCE_QUERY
            variables = {}
        elif operation == "send":
            query = self._SEND_CRYPTO_QUERY

        try:
            response = self._perform_request(query=query, variables=variables)
        except Exception as e:
            raise e
        else:
            return response["data"]


class P2PManager(Manager):
    """
    Handles every peer to peer transactions

    Place limit orders, get market cap history, get placed orders
    """

    _MARKET_ORDER_QUERY = """
        query {
          getMarketBook  {
            dynamicPriceExpiry
            orders {
              edges {
                node {
                  id
                  cryptocurrency
                  coinAmount
                  side
                  status
                  createdAt
                  pricePerCoin
                  priceType
                  staticPrice
                  dynamicExchangeRate
                }
              }
            }
          }
        }
    """

    _DYNAMIC_PRICE_EXPIRY_QUERY = """
        query {
            getOrders(status: open) {
                dynamicPriceExpiry
            }
        }
    """

    _PLACE_LIMIT_ORDER = """
        mutation PostLimitOrder($orderSide: OrderSide!, $coinAmount: BigDecimal!, $cryptocurrency: Cryptocurrency,
        $staticPrice: BigDecimal, $dynamicExchangeRate:BigDecimal, $priceType: PriceType!){
            postLimitOrder(orderSide: $orderSide, coinAmount: $coinAmount, cryptocurrency: $cryptocurrency,
            staticPrice: $staticPrice, priceType: $priceType){
                id
                cryptocurrency
                coinAmount
                side
                status
                createdAt
                pricePerCoin
                priceType
                staticPrice
                dynamicExchangeRate
            }
        }
    """

    _POST_MARKET_ORDER = """
        mutation PostMarketOrder($orderSide: OrderSide!, $coinAmount: BigDecimal!, $cryptocurrency: Cryptocurrency!){
            postMarketOrder(orderSide: $orderSide, coinAmount: $coinAmount, cryptocurrency: $cryptocurrency){
                id
                cryptocurrency
                coinAmount
                side
                status
                createdAt
                pricePerCoin
                priceType
                staticPrice
                dynamicExchangeRate
            }
        }
            """

    def initialize_transaction(self, p2p_transaction):
        data = self.to_json(p2p_transaction)
        operation = data.pop("operation")
        variables = {**data}

        if operation == "plo":
            try:
                if not variables["dynamicExchangeRate"]:
                    variables.pop("dynamicExchangeRate")
                elif not variables["staticPrice"]:
                    variables.pop("staticPrice")
            except:
                pass
            self.post_limit_order(variables)
        elif operation == "pmo":
            self.post_market_order(variables)

    def post_limit_order(self, variables):
        """
        Places limit order for the supplied cryptocurrency.
        Args:
            order_side (str): The side of the order. This could be `buy` or `sell`.
            coin_amount (str): The amount the limit order is based on.
            currency (str): The cryptocurrency involved in the limit order.
            static_price (str, optional): Static price for the cryptocurrency in Naira.
            price_type (str): Static or dynamic price for the cryptocurrency.
        Returns:
            response: A JSON object containing the result from the request.
        """
        query = self._PLACE_LIMIT_ORDER

        try:
            response = self._perform_request(query=query, variables=variables)
        except Exception as e:
            raise e
        else:
            return response["data"]

    def post_market_order(self, variables):
        """
        Places market order for the supplied cryptocurrency.
        Args:
            order_side (str): The side of the order. This could be `buy` or `sell`.
            coin_amount (str): The amount the limit order is based on.
            currency (str): The cryptocurrency involved in the limit order.
        Returns:
            response: A JSON object containing the result from the request.
        """
        query = self._POST_MARKET_ORDER
        try:
            response = self._perform_request(query=query, variables=variables)
        except Exception as e:
            raise e
        else:
            return response["data"]

    def get_placed_orders(self):
        pass

    def get_market_order(self):
        """
        Retrieves market order history.
        Returns:
            response: A JSON object containing response from the request.
        """
        query = self._MARKET_ORDER_QUERY
        variables = {}
        try:
            response = self._perform_request(query=query, variables=variables)
        except Exception as e:
            raise e
        else:
            return response["data"]

    def get_dynamic_price_expiry(self):
        """
        Retrieves when next dynamic prices will be updated
        Returns:
            response: A JSON object containing response from the request.
        """
        query = self._DYNAMIC_PRICE_EXPIRY_QUERY
        variables = {}

        try:
            response = self._perform_request(query=query, variables=variables)
        except Exception as e:
            raise e
        else:
            return response["data"]


class NGNTManager(Manager):
    pass
