# coding: utf-8
import threading
import json
from concurrent.futures import ThreadPoolExecutor
from broker.websockets import BrokerWss
from queue import Queue
import websocket

thread_pool = ThreadPoolExecutor(128)
thread_pool._work_queue
user_data_stream_queue = Queue()


def order_processor(order):
    print("process order: {}".format(order))


class UserDataConsumer(threading.Thread):

    def run(self):
        while True:
            data = user_data_stream_queue.get()
            if data is None:
                continue

            thread_pool.submit(order_processor, data)


def user_data_stream_handler(message):
    print("receive message: {}".format(message))

    if isinstance(message, dict):
        # 返回的是PING消息 不需要发往queue
        return
    elif isinstance(message, list):
        for data in message:
            if isinstance(data, dict) and data.get('e') == 'contractExecutionReport':
                user_data_stream_queue.put(data)
    else:
        # 其它消息
        return


def main():
    # 启动消息消费者
    UserDataConsumer().start()

    entry_point = 'wss://wsapi.bhex.com/openapi/'  # input your broker websocket api url
    rest_entry_point = 'https://api.bhex.com/openapi/'  # input your broker api uri
    api_key = ''
    api_secret = ''

    # 启动WebsocketClient
    ws_client = BrokerWss(entry_point, rest_entry_point, api_key=api_key, secret=api_secret)
    ws_client.user_data_stream(callback=user_data_stream_handler)
    ws_client.start()

    ws = websocket.WebSocketApp()
    ws.run_forever()

if __name__ == '__main__':
    main()
