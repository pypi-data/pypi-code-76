from decouple import config


class BuyCoinConfig:
    """
    Set up buycoin config
    """
    BUYCOIN_PUBLIC_KEY = config('BUYCOIN_PUBLIC_KEY')
    BUYCOIN_SECRET_KEY = config('BUYCOIN_SECRET_KEY')
    BUYCOIN_URL = "https://backend.buycoins.tech/api/graphql"

    def __new__(cls):
        return TypeError('Can\'t create new instance of this class')
