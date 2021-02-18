import logging
import time

from broker.client_v3 import BrokerV3Client

if __name__ == '__main__':
    from broker import broker_log

    broker_log.setLevel(logging.DEBUG)
    broker_log.addHandler(logging.StreamHandler())

    proxies = {
        "http": "",
        "https": "",
    }

    # like: https://api.xxx.yyy/openapi/ where xxx.yyy is your base domain
    entry_point = ''
    b = BrokerV3Client(entry_point,
                       api_key='',
                       secret='',
                       proxies=proxies)

    result = b.order_new(symbol='BTCUSDT', order_side='BUY', order_type='LIMIT', quantity='0.1',
                         price='30000', time_in_force='GTC')

    print(result)

    order_id = result['orderId']

    print(b.order_get(order_id=order_id))

    print(b.order_cancel(order_id=order_id))

    print(b.open_orders(symbol='BTC_USDT'))

    print(b.history_orders(symbol='BTC_USDT'))

    print(b.account())

    print(b.my_trades(symbol='BTC_USDT'))
    # print(result)
