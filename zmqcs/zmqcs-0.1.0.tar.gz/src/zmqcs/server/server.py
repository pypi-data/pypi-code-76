#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#
import queue
from abc import ABC, abstractmethod
import zmq
import threading
import time

from zmqcs.common.message import MessageBase, MessageType, AsyncMSG, CommandAns, ErrorMSG
from zmqcs.common.defaults import Defaults
from zmqcs.server.AsyncStats import AsyncStats
from zmqcs.logs import get_logger


log = get_logger('server')


class zmqServer(ABC):
    def __init__(self, cmd_port=Defaults.repreq_port,
                 async_port=Defaults.pubsub_port):
        self._ports = {'cmd': cmd_port,
                       'async': async_port}
        self._exit = False
        self._ctx = None
        self.rep_req_socket = None
        self.pub_sub_socket = None
        # self.pub_loop = 0
        self._th = []
        self._rcv_timeout = 2000
        self._pub_queue = queue.Queue()
        self._stats = AsyncStats()

    @property
    def stats(self):
        return self._stats.stats

    def start(self):
        logic_th = threading.Thread(target=self._cmd_worker, name='rep_req')
        logic_th.start()
        log.info('Started rep_req socket thread')
        self._th.append(logic_th)
        pub_sub_th = threading.Thread(target=self._pub_sub_worker, name='pub_sub')
        pub_sub_th.start()
        log.info('Started pub_sub socket thread')
        self._th.append(pub_sub_th)

    def exit(self):
        self._exit = True
        log.debug(f"Set exit to True")

    def join(self):
        for el in self._th:
            el.join()
            log.info(f'joined thread {el.name}')
        log.info(f'joined all threads')

    def init_sockets(self):
        self._ctx = zmq.Context()
        self.rep_req_socket = self._ctx.socket(zmq.REP)
        self.rep_req_socket.bind(f"tcp://*:{self._ports['cmd']}")
        self.rep_req_socket.setsockopt(zmq.RCVTIMEO, self._rcv_timeout)

        self.pub_sub_socket = self._ctx.socket(zmq.PUB)
        self.pub_sub_socket.bind(f"tcp://*:{self._ports['async']}")
        log.debug('Initialized sockets')

    def _cmd_worker(self):
        while not self._exit:
            #  Wait for next request from client
            try:
                message = self.rep_req_socket.recv()
                log.debug("Received request: %s ..." % message)
            except zmq.error.Again:
                # log.debug('cmd_worker empty')
                continue
            else:
                # self._rep_req_process_petition runs inside a try catch clause
                s = time.time()
                ans = self._rep_req_process_petition(message)
                et = time.time() - s
                if et > Defaults.exec_time_warning:
                    log.warning(f'message took too long ({et:.2}s) to execute. message: {message}')
                #  Send reply back to client
                self.rep_req_socket.send(ans.as_bytes)
        log.info("Exited rep_req_logic loop")

    @abstractmethod
    def execute_command(self, cmd_msg):
        # This must be implemented on the higher level server layer
        # cmd_msg will be an instance of a subclass of CommandMSG
        # It must return either an exception or a json serializable value
        pass

    def _rep_req_process_petition(self, message):
        # This function receives the bytes received at zmq socket and reconstruct a CommandMSG or a subclass of it
        # When the message it is reconstructed, it calls self.execute_command(message) and returns back to the server
        # an answer of the command or an error to the client
        answer = None
        #print(f"this is a message {message}")
        try:
            msg = MessageBase.from_bytes(message)
            if msg.type == MessageType.CMD:
                answer = CommandAns.from_cmdmsg(msg)
                answer.set_start_time()
                try:
                    answer.ans = self.execute_command(cmd_msg=msg)

                except Exception as ex:
                    log.exception('Exception while processing command')
                    answer.error = str(ex)
            else:
                answer = ErrorMSG(msg=f"Received message is not a Command. Received type {msg.type}")
        except Exception as ex:
            log.exception('Exception while reconstructing message')
            answer = ErrorMSG(f"Exception happened: {str(ex)}")
        finally:
            if answer is None:
                answer = ErrorMSG(msg="Unknown thing happened. Answer was not set")
                log.debug(f"There was no answer from the command {msg.as_json}")
            if isinstance(answer, CommandAns):
                answer.set_end_time()
            return answer

    def pub_async(self, topic, value):
        # value must be a json serializable item
        self._pub_queue.put((topic, value))
        self._stats.pub(topic)

    def _pub_sub_worker(self):
        # self.pub_loop = 0
        while not self._exit:
            try:
                topic, value = self._pub_queue.get(block=True, timeout=2)
                async_msg = AsyncMSG(topic=topic, value=value)
            except queue.Empty:
                # we put a timeout so we can check for _exit condition
                continue
            else:
                tmp = async_msg.pub_serialize()
                self.pub_sub_socket.send(tmp)
                # log.debug(f"PUB Thread -  {tmp}")
                # self.pub_loop += 1
                # if self.pub_loop % 10 == 0:
                #     log.debug(f"PUB Thread -  {self.pub_loop}")
        log.info(f"Exited pub_sub_worker loop")
