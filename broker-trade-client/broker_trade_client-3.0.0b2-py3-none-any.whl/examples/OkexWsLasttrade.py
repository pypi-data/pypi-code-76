import copy
import json
import logging
import threading
import time
import zlib



from datetime import datetime
from queue import Queue

import websocket
import ssl



class OkexWsLasttrade:
    def __init__(self, target_ticker, task_queue, task_queue1):
        self.target_ticker = target_ticker
        self.task_queue = task_queue          # this is the queue that here we put data into
        self.task_queue1 = task_queue1          # this is the queue that here we put data into, for dumping must orders

        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://real.okex.com:8443/ws/v3",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        # ws.on_open = self.on_open
        # ws.run_forever(http_proxy_host="127.0.0.1", http_proxy_port=1087, sslopt={"cert_reqs": ssl.CERT_NONE})
        self.recent_bid1ask1 = {
                        'bid1': 0,
                        'ask1': 10000000,
                        'mid_price': 0,
                        'msg_ts': -1,
                    }
        self.recent_lasttrade = {
                        'bid1': 0,
                        'ask1': 10000000,
                        'mid_price': 0,
                        'msg_ts': -1,
                    }
        self.last_update_from_depth = True


    def inflate(self, data):
        decompress = zlib.decompressobj(
                -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated


    # This is the "callback" function: after receiving the msg from subscriber, we just put into the queue
    def on_message(self, message):
        try:
            time_start = time.time()
            msg = json.loads((self.inflate(message)))
            time_end = time.time()
            print('it took %s ms to inflate\n' % (time_end - time_start) * 1000)

            if 'data' in msg.keys():
                if msg['table'] == 'swap/depth5':
                    crt_bid1 = float(msg['data'][0]['bids'][0][0])
                    crt_ask1 = float(msg['data'][0]['asks'][0][0])
                    crt_mid = (crt_bid1 + crt_ask1) / 2
                    if (self.recent_bid1ask1['bid1'] != crt_bid1) or (self.recent_bid1ask1['ask1'] != crt_ask1) or (not self.last_update_from_depth):
                        # record the msg into the Queue
                        msg_for_queue = {
                            'bid1': crt_bid1,
                            'ask1': crt_ask1,
                            'mid_price': crt_mid,
                            'msg_ts': datetime.strptime(msg['data'][0]['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                        }
                        self.task_queue.put(msg_for_queue)
                        self.task_queue1.put(msg_for_queue)
                        self.recent_bid1ask1 = copy.deepcopy(msg_for_queue)
                        self.last_update_from_depth = True
                        # print('updated DEPTH - %s' % msg_for_queue)
                    else:
                        # print('skipping data due to it is not really updated DEPTH - %s' % msg)
                        pass

                elif msg['table'] == 'swap/trade':
                    crt_price = float(msg['data'][0]['price'])
                    if (self.recent_lasttrade['mid_price'] != crt_price) or (self.last_update_from_depth):
                        msg_for_queue = {
                            'bid1': crt_price,
                            'ask1': crt_price,
                            'mid_price': crt_price,
                            'msg_ts': datetime.strptime(msg['data'][0]['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                        }
                        self.task_queue.put(msg_for_queue)
                        self.task_queue1.put(msg_for_queue)
                        self.recent_lasttrade = copy.deepcopy(msg_for_queue)
                        self.last_update_from_depth = False
                        # print('updated TRADE - %s' % msg_for_queue)
                    else:
                        # print('skipping data due to it is not really updated TRADE - %s' % msg)
                        pass
                else:
                    pass

            elif 'event' in msg.keys():
                logging.info(msg)
            else:
                logging.error(msg)
        except Exception as e:
            logging.error('on_message function has some issue - %s', e)


    def on_error(self, error):
        logging.error(error)


    def on_close(self):
        logging.error("### closed ###")


    def on_open(self):
        crt_ticker = self.target_ticker
        ws = self.ws
        def run(crt_ticker):
            sub_msgs = ["swap/depth5:" + crt_ticker, "swap/trade:" + crt_ticker]
            ws.send(json.dumps({"op": "subscribe", "args": sub_msgs}))
        threading.Thread(target=run, args=(crt_ticker,)).start()


task_queue = Queue()
task_queue1 = Queue()

okWsDepth = OkexWsLasttrade(target_ticker='BTC-USD-SWAP', task_queue=task_queue, task_queue1=task_queue1)
okWsDepth.ws.on_open = okWsDepth.on_open
okWsDepth.ws.run_forever(http_proxy_host="127.0.0.1", http_proxy_port=1087, sslopt={"cert_reqs": ssl.CERT_NONE})


