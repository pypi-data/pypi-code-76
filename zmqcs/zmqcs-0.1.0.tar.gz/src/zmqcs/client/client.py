#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import threading
import queue

from zmqcs.common.message import MessageBase, CommandMSG, AsyncMSG
from zmqcs.common.defaults import Defaults
from zmqcs.client.callbacks import AsyncCallback
from zmqcs.client.stats import AsyncStats
from zmqcs.logs import get_logger

log = get_logger('zmqClient')


class zmqClient(object):
    def __init__(self, en_async=True, async_timeout=Defaults.sub_timeout):
        self.connected = False
        self._ctx = None
        self._req_socket = None
        self._sub_socket = None
        self._async_enabled = en_async
        self._exit = False
        self._async_th = None
        # To allow self._sub_socket to be used only from its thread once started we create a queue
        self._async_queue = queue.Queue()
        self._as = AsyncStats()
        self._async_timeout = async_timeout
        self._callbacks = {}

    def connect(self, ip='localhost',
                req_port=Defaults.repreq_port,
                async_port=Defaults.pubsub_port):
        self._ctx = zmq.Context()
        #  Socket to talk to server
        self._req_socket = self._ctx.socket(zmq.REQ)
        # self._req_socket.setsockopt(zmq.RCVTIMEO, 1000)
        self._req_socket.connect(f"tcp://{ip}:{req_port}")
        log.debug(f"Connected REQ socket to port {req_port}")

        if self._async_enabled:
            self._sub_socket = self._ctx.socket(zmq.SUB)
            self._sub_socket.connect(f"tcp://{ip}:{async_port}")
            self._sub_socket.setsockopt(zmq.RCVTIMEO, self._async_timeout)
            log.debug(f"Connected SUB socket to port {async_port}")
        log.info('Initialized sockets')
        self.connected = True

    def close(self):
        if self._async_th:
            self._exit = True
            log.debug('Set to exit loop')
            self._async_th.join()
            log.debug('Joined pubsub thread')
        self.connected = False
        if self._req_socket:
            self._req_socket.close()
            self._req_socket = None
        # self._sub_socket is closed when leaving the thread
        if self._ctx:
            self._ctx = None

    def async_subscribe(self, topic, callback):
        self._async_queue.put((topic, callback))

    def _proc_async_queue(self):
        while True:
            try:
                topic, callback = self._async_queue.get(block=False)
            except queue.Empty:
                return
            else:
                try:
                    self._async_subscribe(topic, callback)
                except:
                    log.exception(f"Failed to register callback to topic '{topic}'")

    def _async_subscribe(self, topic, callback):
        """
        This is called from the async thread
        """
        if self._async_enabled:

            log.debug(f"Petition to subscribe to topic '{topic}'")
            if not isinstance(topic, bytes):
                topic = topic.encode('utf-8')

            self._as.new_topic(topic)

            if not issubclass(type(callback), AsyncCallback):
                raise Exception("callback must be of type AsyncCallback")
            if topic not in self._callbacks:
                self._callbacks[topic] = []
            self._callbacks[topic].append(callback)
            self._sub_socket.subscribe(topic)
            self._as.cb_reg(topic)
            log.debug(f"Subscribed callback to topic '{topic}'")
        else:
            log.error(f"Tried to subscribe to topic '{topic}' but async is not enabled")

    def _process_callbacks(self, topic, async_msg):
        if topic in self._callbacks:
            for cb in self._callbacks[topic]:
                try:
                    cb.run(topic, async_msg)
                    self._as.cb_call(topic)
                except:
                    log.exception(f"Exception when executing callback for topic '{topic}'")
                    self._as.exception(topic)
        else:
            self._as.unknown_topic(topic)

    def async_loop(self):
        if self._async_enabled:
            if not self._sub_socket:
                raise Exception('Async socket not initialized')
            while not self._exit:
                self._proc_async_queue()
                try:
                    # topic, msg_bytes = self._sub_socket.recv_multipart()
                    topic = None
                    recv_bytes = self._sub_socket.recv()
                    try:
                        topic, async_msg = AsyncMSG.sub_deserialize(recv_bytes)
                        # log.debug(f"Received async for topic '{topic}'")
                    except:
                        log.exception(f"Could not recover AsyncMSG. Received: {recv_bytes}")
                        self._as.bad_msg(topic)
                        continue
                    else:
                        self._process_callbacks(topic=topic, async_msg=async_msg)
                except zmq.error.Again:
                    continue
            log.info('Out of pubsub loop')
            if self._sub_socket:
                self._sub_socket.close()
                self._sub_socket = None
                log.info('Closed sub socket')

        else:
            log.error('Async loop was executed but async is not enabled')

    def start(self):
        self._exit = False
        if self._async_enabled:
            self._async_th = threading.Thread(target=self.async_loop)
            self._async_th.start()
            log.info("Started pubsub thread")
        else:
            log.error('Async is not enabled, can\'t start its thread')

    def _command(self, cmd):
        """Send a CommandMSG to the server"""
        if not issubclass(type(cmd), CommandMSG):
            log.debug('Bad command, command should be of type CommandMSG')
            raise Exception("Bad command, command should be of type CommandMSG")
        self._req_socket.send(cmd.as_bytes)
        ans_bytes = self._req_socket.recv()
        # log.debug(f"Received answer from server for command '{cmd.command}")
        return MessageBase.from_bytes(ans_bytes)

    def get_async_stats(self):
        return self._as.as_json()
