import math
from types import SimpleNamespace
import time
import logging
from dataclasses import dataclass
from typing import Any
from datetime import datetime
from twisted.internet import reactor
import json
import ssl
import zlib
from threading import Thread

from gateway.okex.okex.swap_api import SwapAPI
import websocket
from gateway.base_gateway import BaseGateway
from datatype.object import ReqFuncReturn, SwapTickerObj, PriceObj, DepthObj, AssetObj, SwapAssetObj, PositionObj, OrderObj, TradesObj
from datatype.const import *
from engine.event_engine import EventEngine, EventTypes, Event




@dataclass(frozen=True)
class OkexConst:
    """
    contains all constants from okex api terminology convention
    """
    order_type: SimpleNamespace = SimpleNamespace(**{'Normal': '0', 'Post_Only': '1', 'FOK': '2', 'IOC': '3'})
    type: SimpleNamespace = SimpleNamespace(**{'open_long': '1', 'open_short': '2',
                                               'close_long': '3', 'close_short': '4'})
    state: SimpleNamespace = SimpleNamespace(**{'Failed': '-2', 'Canceled': '-1', 'Open': '0',
                                                 'Partially_Filled': '1', 'Fully_Filled': '2',
                                                 'Submitting': '3', 'Canceling': '4', 'Incomplete': '6',
                                                 'Complete': '7'})

    error: SimpleNamespace = SimpleNamespace(**{'ORDER_NO_EXIST': 35029, 'ORDER_FILLED': 35044, })





OKEX_CONST = OkexConst()



class OkexSwapGateway(BaseGateway):
    """
    Realization of Okex gateway. Outputs from this class are in
    this project's standard system format.
    """
    def __init__(self, login: dict, event_engine: EventEngine, event_types: EventTypes):
        """Constructor"""
        super().__init__()
        self.login = login                  # Here login just need the api connecting information, nothing else
        self.event_engine = event_engine
        self.event_types = event_types

        self.rest_api = SwapAPI(
            api_key=self.login['api_key'],
            api_seceret_key=self.login['secret'],
            passphrase=self.login['passphrase'],
            proxies=self.login['proxies'],
            use_server_time=True,
        )
        websocket.enableTrace(True)
        self.ws_api = websocket.WebSocketApp(
            url=self.login['url'],
        )
        self.ws_subscription_list = []  # this is the subscription list we pass into okex websocket subscription request
        self.ts_offset = 0          # ts_server + ts_offset = ts_local, namely, calibrating server time to local time


    def _is_return_fail(self, api_return: Any) -> bool:
        """
        Check whether api revoke return error or not.  TODO: what to do?
        """
        if isinstance(api_return, dict) and ('error_code' in api_return.keys()):
            # return error code and thus revoke failed
            if api_return['error_code'] == '0':
                # no error so, return is not failed
                return False
            else:
                return True
        else:
            return False


    def query_time(self) -> ReqFuncReturn:
        """
        TODO: No such function from Okex rest api
        """
        return ReqFuncReturn(is_succeed=False, data=UNDEFINED_FLOAT)


    def query_info(self, ticker: str) -> ReqFuncReturn:
        """
        Public end point
        Get config information for interested ticker
        """
        try:
            api_return = self.rest_api.get_instruments()
        except Exception as e:
            logging.error(ERROR_REVOKE_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        if self._is_return_fail(api_return=api_return):
            logging.error(ERROR_RETURN_ + str(api_return))
            return ReqFuncReturn(is_succeed=False, data=None)
        # standardize api return data to our system format data
        try:
            info_swap = api_return
            for data in info_swap:
                if data['instrument_id'] == ticker:
                    ticker_info = SwapTickerObj(
                        ticker=data['instrument_id'],
                        underlying=data['underlying_index'],
                        base_asset=data['instrument_id'],
                        base_step=float(data['size_increment']),
                        base_precision=int(-round(math.log(float(data['size_increment']), 10), 0)),
                        quote_asset=data['quote_currency'],
                        quote_step=float(data['tick_size']),
                        quote_precision=int(-round(math.log(float(data['tick_size']), 10), 0)),
                        min_price=UNDEFINED_FLOAT,
                        min_qty=UNDEFINED_FLOAT,
                        min_amt=UNDEFINED_FLOAT,
                        margin_asset=data['settlement_currency'],
                        margin_step=UNDEFINED_FLOAT,
                        margin_precision=int(UNDEFINED_FLOAT),
                        index=data['underlying'],
                        multiplier=float(data['contract_val']),
                        is_inverse=True if (data['is_inverse'] == 'true') else False,
                    )
                    return ReqFuncReturn(is_succeed=True, data=ticker_info)
        except Exception as e:
            logging.error(ERROR_DATA_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        # if code goes here and not found ticker_info for the desired ticker, something is wrong
        logging.error(ERROR_DATA_ + 'selected ticker %s is not found in infor_swap data' % ticker)
        return ReqFuncReturn(is_succeed=False, data=None)


    def query_index(self, ticker: str) -> ReqFuncReturn:
        """
        Public end point
        Get current index value
        This rest query automatically put result into event_engine
        """
        try:
            api_return = self.rest_api.get_index(instrument_id=ticker)
        except Exception as e:
            logging.error(ERROR_REVOKE_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        if self._is_return_fail(api_return=api_return):
            logging.error(ERROR_RETURN_ + str(api_return))
            return ReqFuncReturn(is_succeed=False, data=None)
        # standardize api return data to our system format data
        try:
            data = PriceObj(
                ts_server=datetime.strptime(api_return['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                ticker=api_return['instrument_id'],
                value=float(api_return['index']),
            )
        except Exception as e:
            logging.error(ERROR_DATA_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        event = Event(type=self.event_types.data_index_rest, data=data)
        self.event_engine.put(event=event)
        return ReqFuncReturn(is_succeed=True, data=data)


    def query_depth(self, ticker: str, limit: int) -> ReqFuncReturn:
        """
        Public end point
        Get current orderbook (depth)
        This rest query automatically put result into event_engine
        """
        try:
            api_return = self.rest_api.get_depth(instrument_id=ticker, size=limit)
        except Exception as e:
            logging.error(ERROR_REVOKE_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        if self._is_return_fail(api_return=api_return):
            logging.error(ERROR_RETURN_ + str(api_return))
            return ReqFuncReturn(is_succeed=False, data=None)
        # standardize api return data to our system format data
        try:
            data = DepthObj(
                ts_server=datetime.strptime(api_return['time'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                ticker=ticker,
                bids=[dict(zip([PRICE_, QTY_], [float(d[0]), float(d[1])])) for d in api_return['bids']],
                asks=[dict(zip([PRICE_, QTY_], [float(d[0]), float(d[1])])) for d in api_return['asks']],
            )
        except Exception as e:
            logging.error(ERROR_DATA_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        event = Event(type=self.event_types.data_depth_rest, data=data)
        self.event_engine.put(event=event)
        return ReqFuncReturn(is_succeed=True, data=data)


    def query_account(self, ticker: str) -> ReqFuncReturn:
        """
        Private end point
        Query account balance for specific asset (token)
        This rest query automatically put result into event_engine
        """
        try:
            ts_req = time.time()
            api_return = self.rest_api.get_coin_account(instrument_id=ticker)
            ts_recv = time.time()
        except Exception as e:
            logging.error(ERROR_REVOKE_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        if self._is_return_fail(api_return=api_return):
            logging.error(ERROR_RETURN_ + str(api_return))
            return ReqFuncReturn(is_succeed=False, data=None)
        # standardize api return data to our system format data
        try:
            d = api_return['info']
            data = AssetObj(
                # TODO: think of how we should record and maintain the "account", include unrealize pnl or not
                # TODO: also okex api variable interpretation has problems
                ts_server=datetime.strptime(d['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                asset=d['currency'],
                total=float(d['equity']),
                avail=float(d['total_avail_balance']) - float(d['margin_frozen']),
                locked=float(d['margin']) + float(d['margin_frozen']),
            )
        except Exception as e:
            logging.error(ERROR_DATA_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        event = Event(type=self.event_types.data_acct_rest, data=data)
        self.event_engine.put(event=event)
        return ReqFuncReturn(is_succeed=True, data=data)


    def query_position(self, ticker: str) -> ReqFuncReturn:
        """
        Private end point
        Query holding position for specific ticker (symbol_id)
        This rest query automatically put result into event_engine
        """
        try:
            api_return = self.rest_api.get_specific_position(instrument_id=ticker)
        except Exception as e:
            logging.error(ERROR_REVOKE_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        if self._is_return_fail(api_return=api_return):
            logging.error(ERROR_RETURN_ + str(api_return))
            return ReqFuncReturn(is_succeed=False, data=None)
        # standardize api return data to our system format data
        try:
            # initialize pos_long and pos_short with 0 balance and then update them using api_return
            pos_long = SwapAssetObj(
                ts_server=datetime.strptime(api_return['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                asset=ticker,
                total=0,
                avail=0,
                locked=0,
                avg_cost=UNDEFINED_FLOAT,
                liq_price=UNDEFINED_FLOAT,
            )
            pos_short = SwapAssetObj(
                ts_server=datetime.strptime(api_return['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                asset=ticker,
                total=0,
                avail=0,
                locked=0,
                avg_cost=UNDEFINED_FLOAT,
                liq_price=UNDEFINED_FLOAT,
            )
            for data in api_return['holding']:
                if data['side'] == 'long':
                    pos_long.total = float(data['position'])
                    pos_long.avail = float(data['avail_position'])
                    pos_long.locked = float(data['position']) - float(data['avail_position'])
                    pos_long.avg_cost = float(data['avg_cost'])
                    pos_long.liq_price = float(data['liquidation_price'])
                elif data['side'] == 'short':
                    pos_short.total = float(data['position'])
                    pos_short.avail = float(data['avail_position'])
                    pos_short.locked = float(data['position']) - float(data['avail_position'])
                    pos_short.avg_cost = float(data['avg_cost'])
                    pos_short.liq_price = float(data['liquidation_price'])
                else:
                    pass
            pos_net = SwapAssetObj(
                ts_server=datetime.strptime(api_return['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                asset=ticker,
                total=pos_long.total - pos_short.total,
                avail=UNDEFINED_FLOAT,  # TODO: optimize avail, locked, avg_cost, liq_price logic
                locked=UNDEFINED_FLOAT,
                avg_cost=UNDEFINED_FLOAT,
                liq_price=UNDEFINED_FLOAT,
            )
            data = PositionObj(
                ts_server=datetime.strptime(api_return['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                ticker=ticker,
                net=pos_net,
                long=pos_long,
                short=pos_short,
            )
        except Exception as e:
            logging.error(ERROR_DATA_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        event = Event(type=self.event_types.data_posn_rest, data=data)
        self.event_engine.put(event=event)
        return ReqFuncReturn(is_succeed=True, data=data)


    def query_orders(self, ticker: str, limit: int) -> ReqFuncReturn:
        """
        Private end point
        Query open orders for specific ticker (symbol_id)
        """
        try:
            api_return = self.rest_api.get_order_list(instrument_id=ticker, status=OKEX_CONST.state.Incomplete, limit=limit)  # status = 6 means `NEW` + `PARTIALLY_FILLED`
        except Exception as e:
            logging.error(ERROR_REVOKE_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)
        if self._is_return_fail(api_return=api_return):
            logging.error(ERROR_RETURN_ + str(api_return))
            return ReqFuncReturn(is_succeed=False, data=None)
        # standardize api return data to our system format data
        try:
            open_orders = {}
            for order_raw in api_return['order_info']:
                order = OrderObj(
                    price=float(order_raw['price']),
                    qty=float(order_raw['size']) - float(order_raw['filled_qty']),
                    side=SIDE_LONG if order_raw['type'] in [OKEX_CONST.type.open_long, OKEX_CONST.type.close_short] else SIDE_SHORT,
                    ticker=ticker,
                    cid=order_raw['client_oid'],
                    cat_key=CAT_UNDEFINED,
                    lever=UNDEFINED_FLOAT,      # TODO: okex has very weird leverage system
                    margin=UNDEFINED_FLOAT,     # TODO: what to do
                    is_close=True if order_raw['type'] in [OKEX_CONST.type.close_long, OKEX_CONST.type.close_short] else False,
                    ts_create=datetime.strptime(order_raw['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                    ext={
                        'client_oid': order_raw['client_oid'],
                        'size': order_raw['size'],
                        'type': order_raw['type'],
                        'price': order_raw['price'],
                        'instrument_id': order_raw['instrument_id'],
                        'order_type': order_raw['order_type'],
                        'order_id': order_raw['order_id'],
                    },
                )
                open_orders.update({order.cid: order})          # a dict of Order
            return ReqFuncReturn(is_succeed=True, data=open_orders)
        except Exception as e:
            logging.error(ERROR_DATA_ + str(e))
            return ReqFuncReturn(is_succeed=False, data=None)


    def send_order(self, order: OrderObj) -> ReqFuncReturn:
        """
        Send a new order to server.
        This function takes order as an input, and it is actually
        pass by reference, revise it's attributes and return it out
        Only need to put event into event engine when placing order succeeded, since if this is failed we don't need
        to put the order into outstanding orders dict in baes_worker
        """
        if order.side == SIDE_LONG:
            if order.is_close:
                order_side = OKEX_CONST.type.close_short        # BHEX_CONST.side.BUY_CLOSE
            else:
                order_side = OKEX_CONST.type.open_long          # BHEX_CONST.side.BUY_OPEN
        else:
            if order.is_close:
                order_side = OKEX_CONST.type.close_long         # BHEX_CONST.side.SELL_CLOSE
            else:
                order_side = OKEX_CONST.type.open_short         # BHEX_CONST.side.SELL_OPEN
        order.ext = {
            'client_oid': order.cid,
            'size': order.qty,
            'type': order_side,
            'price': order.price,
            'instrument_id': order.ticker,
            'order_type': OKEX_CONST.order_type.Normal,
            'order_id': '',
        }
        try:
            api_return = self.rest_api.take_order(instrument_id=order.ext['instrument_id'],
                                                  client_oid=order.ext['client_oid'],
                                                  size=order.ext['size'],
                                                  otype=order.ext['type'],
                                                  price=order.ext['price'],
                                                  match_price='0'
                                                  )           # TODO: what is this
        except Exception as e:
            logging.error(ERROR_REVOKE_ + str(e) + ' - ' + str(order))
            return ReqFuncReturn(is_succeed=False, data=None)
        if self._is_return_fail(api_return=api_return):
            logging.error(ERROR_RETURN_ + str(api_return) + ' - ' + str(order))
            return ReqFuncReturn(is_succeed=False, data=None)
        # standardize api return data to our system format data
        is_succeed = (api_return['result'] == 'true')    # TODO: need to see if this criterion is solid
        order.update_oid_ts(oid=api_return['order_id'], ts_create=time.time())      # TODO: this is using the local time
        gw_return = ReqFuncReturn(is_succeed=is_succeed, data=order)
        if is_succeed:
            logging.info('successfully creating order with cid  = %s' % order.cid)
        else:
            logging.error(ERROR_UNKNOWN_ + api_return + ' - ' + str(order))
        return gw_return


    def cancel_order(self, order: OrderObj) -> ReqFuncReturn:
        """
        Cancel an existing order.
        Bhex will try to cancel by order_id, if not succeeded then try client order id
        About why event is put into events even when cancel is failed:
        In base_worker, when calling this method, the order is temporarily removed from the outstanding order dict
        so if this cancel is failed, we need to "receive" this info and put the order back into the dict again
        TODO: revisit what is defined to be cancel order failed? not on ob, or has already been canceled, has been filled, should not be failed
        """
        try:
            api_return = self.rest_api.revoke_order(instrument_id=order.ticker, order_id=order.ext['order_id'], client_oid=order.ext['client_oid'])
        except Exception as e:
            logging.error(ERROR_REVOKE_ + str(e) + ' - ' + str(order))
            gw_return = ReqFuncReturn(is_succeed=False, data=order)
            return gw_return
        if self._is_return_fail(api_return=api_return):
            # these four cases actually we treat it as successfully canceled.
            if api_return['error_code'] in [OKEX_CONST.error.ORDER_NO_EXIST, OKEX_CONST.error.ORDER_FILLED]:
                logging.error('successfully canceling order with cid  = %s, api_return  = %s' % (order.cid, api_return))
                gw_return = ReqFuncReturn(is_succeed=True, data=order)
                return gw_return
            else:
                logging.error(ERROR_RETURN_ + str(api_return) + ' - ' + str(order))
                gw_return = ReqFuncReturn(is_succeed=False, data=order)
                return gw_return
        # standardize api return data to our system format data
        # if we place an order and it is filled instantly, then we try to cancel it, it should be regarded as success
        is_succeed = (api_return['result'] == 'true')       # TODO: need to see if this criterion is solid
        if is_succeed:
            logging.info('successfully canceling order with cid  = %s' % order.cid)
        else:
            logging.error(ERROR_UNKNOWN_ + str(api_return) + ' - ' + str(order))
        gw_return = ReqFuncReturn(is_succeed=is_succeed, data=order)
        return gw_return


    def _on_depth(self, message: dict) -> None:
        """
        Websocket callback function for depth subscription
        message is a dict, with keys = ['symbol', 'topic', 'params', 'data', 'f', 'shared']
        where message['data'] is a list with len 1
        """
        if 'data' not in message.keys():
            pass
        else:
            depth_raw = message['data'][0]
            event = Event(
                type=self.event_types.data_depth_ws,
                data=DepthObj(
                    ts_server=datetime.strptime(depth_raw['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                    ticker=depth_raw['instrument_id'],
                    bids=[dict(zip([PRICE_, QTY_], [float(d[0]), float(d[1])])) for d in depth_raw['bids'][0:DEFAULT_DEPTH]],         # TODO: parameterize this if needed
                    asks=[dict(zip([PRICE_, QTY_], [float(d[0]), float(d[1])])) for d in depth_raw['asks'][0:DEFAULT_DEPTH]],
                )
            )
            # if event.type == 'DATA::DEPTH::WS::BTC-USD-SWAP::OKEX::okex_test':
            #     logging.critical('time diff = %s, size of global event engine = %s' % (
            #     time.time() - event.data.ts_server, event.data.bids[0]['price']))
            self.event_engine.put(event=event)


    def subscribe_depth(self, ticker: str) -> None:
        """
        Public end point subscription
        Subscribe to the depth channel
        """
        sub_channel = "swap/depth5:" + ticker
        self.ws_subscription_list.append(sub_channel)



    def _on_trades(self, message: dict) -> None:
        """
        Websocket callback function for public trades subscription
        message is a dict, with keys = ['table', 'data']
        where message['data'] is a list with len 1
        """
        if 'data' not in message.keys():
            pass
        else:
            trades_raw = message['data'][0]
            event = Event(
                type=self.event_types.data_trades_ws,
                data=TradesObj(
                    ts_server=datetime.strptime(trades_raw['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                    ticker=trades_raw['instrument_id'],
                    price=float(trades_raw['price']),
                    qty=float(trades_raw['size']),
                )
            )
            self.event_engine.put(event=event)


    def subscribe_trades(self, ticker: str) -> None:
        """
        Public end point subscription
        Subscribe to the public trades channel
        """
        sub_channel = "swap/trade:" + ticker
        self.ws_subscription_list.append(sub_channel)


    def _inflate(self, data):
        """
        Helper function from okex to decompress the raw pushed data from okex websocket subscription
        """
        decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated


    def _on_message(self, message) -> None:
        """
        This is the call back function from okex websocket connection
        """
        inflated_msg = json.loads((self._inflate(data=message)))
        logging.critical(inflated_msg)
        if 'table' in inflated_msg.keys():
            if inflated_msg['table'] == 'swap/depth5':
                self._on_depth(message=inflated_msg)
            elif inflated_msg['table'] == 'swap/trade':
                self._on_trades(message=inflated_msg)
            else:
                pass


    def start_subscription(self) -> None:
        """
        Start connection and getting pushed data from server
        No blocking for bhex ws subscription, thus no need to put into thread again
        """
        def on_open(ws):
            try:
                ws.send(json.dumps({"op": "subscribe", "args": self.ws_subscription_list}))
            except Exception as e:
                logging.error(ERROR_SUBSCRIPTION_ + str(e))

        def on_error(ws, error):
            logging.error(ERROR_SUBSCRIPTION_ + str(error))

        def on_close(ws):
            logging.error("### closed ###")

        def okex_run_forever():
            """
            Note that run_forever() method is blocking, so we need to wrap this into a thread and run
            """
            while True:
                try:
                    if self.login['proxies']['http'] == "":
                        self.ws_api.run_forever()
                    else:
                        http_proxy_host = self.login['proxies']['http'].split(':')[0]
                        http_proxy_port = self.login['proxies']['http'].split(':')[1]
                        self.ws_api.run_forever(http_proxy_host=http_proxy_host, http_proxy_port=http_proxy_port,
                                                sslopt={"cert_reqs": ssl.CERT_NONE})
                except Exception as e:
                    logging.error(ERROR_SUBSCRIPTION_ + str(e))

        self.ws_api.on_open = on_open
        self.ws_api.on_message = self._on_message
        self.ws_api.on_error = on_error
        self.ws_api.on_close = on_close
        # use a thread to start the run_forever, since the run_forever() method itself is blocking
        Thread(target=okex_run_forever).start()


    def stop(self) -> None:
        """
        Close connection
        """
        # self.ws_api.close()
        # # reactor.callFromThread(reactor.stop)
        pass


    def test_print_event(self, event: Event) -> None:
        """
        A test function that satisfies HandlerType and consumes queue in event_engine
        This function simply prints out the input event
        """
        print('testing printing event - %s' % event)