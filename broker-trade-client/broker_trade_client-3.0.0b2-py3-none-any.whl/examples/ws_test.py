import json
import ssl
import threading
import time
import zlib
import websocket


# msg = {'table': 'swap/depth5',
#  'data': [{'asks': [['9775.7', '475', '0', '11'],
#     ['9776.3', '1', '0', '1'],
#     ['9776.5', '2', '0', '2'],
#     ['9777', '1', '0', '1'],
#     ['9777.3', '1', '0', '1']],
#    'bids': [['9775.6', '4520', '0', '40'],
#     ['9775.5', '1', '0', '1'],
#     ['9775.4', '1', '0', '1'],
#     ['9775.3', '163', '0', '1'],
#     ['9775.2', '73', '0', '2']],
#    'instrument_id': 'BTC-USD-SWAP',
#    'timestamp': '2020-02-17T07:53:41.086Z'}]}

# This is the "callback" function: after receiving the msg from subscriber, we just put into the queue
def on_message(ws, message):
    print("nihao: " + message)

def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('''{"symbol": "BTC_USDT", "req": "get.deal"}''')
    print('on_open')


websocket.enableTrace(False)
ws = websocket.WebSocketApp("wss://wbs.mxcio.co/raw/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
ws.on_open = on_open
# ws.run_forever(http_proxy_host="127.0.0.1", http_proxy_port=1087, sslopt={"cert_reqs": ssl.CERT_NONE})
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


