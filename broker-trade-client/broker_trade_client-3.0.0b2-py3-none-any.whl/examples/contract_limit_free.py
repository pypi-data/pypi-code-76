import logging
import time

from multiprocessing import Queue

q = Queue()
q.put(dict(a=1, b=3))



from broker.client import BrokerContractClient
from broker.exceptions import BrokerRequestException, BrokerApiException

if __name__ == '__main__':
    from broker import broker_log

    # BrokerContractClient.init_connection_args(1, 10)

    broker_log.setLevel(logging.DEBUG)
    broker_log.addHandler(logging.StreamHandler())

    proxies = {
        "http": '',
        "https": '',
    }

    entry_point = 'https://api.bhexb.com/openapi'  # enter your open api entry point

    b = BrokerContractClient(entry_point,
                             api_key='OOzH2ZwEisOjCC8DTHfWTRGGt35zhQZPfBiIwNMOjSYe8YVrUbF8Z707dFTSNbd6',
                             secret='lx2daMTOyol3GWdduIAzPZ9FXcRZGE9Q3IPbhj7rMAZ6Ztah58HjpL0X2iB7zPME',
                             proxies=proxies)
    b1 = BrokerContractClient(entry_point,
                              api_key='',
                              secret='',
                              proxies=proxies)

    try:
        cid = int(time.time()*1000)
        r = b.order_new(symbol='BTC-PERP-BUSDT', clientOrderId=cid, side='BUY_OPEN', orderType='LIMIT',
                        quantity='10', price='5000', leverage='5', timeInForce='GTC', triggerPrice=None)
        print(r)

        # time.sleep(1)

        print(b.order_cancel(r['orderId']))

        # cid1 = int(time.time()*1000)
        # r1 = b1.order_new(symbol='BTC0808', clientOrderId=cid1, side='SELL_OPEN', orderType='LIMIT_FREE',
        #                   quantity='10', price='5381', leverage='5', timeInForce='GTC', triggerPrice=None)
        # print(r1)
    except BrokerRequestException as bre:
        logging.error(bre)
    except BrokerApiException as bae:
        logging.error(bae)
