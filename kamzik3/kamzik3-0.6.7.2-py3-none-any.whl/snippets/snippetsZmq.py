from collections import deque
from time import perf_counter_ns, sleep

import zmq

from kamzik3.constants import WORKER_READY, MSG_TERMINATE, MSG_EMPTY


class Worker:
    running = False

    def __init__(self, id, master_host, master_port, zmq_context=None):
        self.instructions_set = []
        self.zmq_context = zmq_context
        self.master_host = master_host
        self.master_port = master_port
        self.id = id.encode()

    def _init_socket(self):
        if self.zmq_context is None:
            self.zmq_context = zmq.Context.instance()

        self.socket_worker = self.zmq_context.socket(zmq.REQ)
        self.socket_worker.setsockopt(zmq.IDENTITY, self.id)
        self.socket_worker.connect("tcp://{}:{}".format(self.master_host, self.master_port))

    def run(self):
        self.running = True
        self._init_socket()
        self.socket_worker.send_multipart([WORKER_READY] + self.instructions_set)
        while self.running:
            request = self.socket_worker.recv_multipart()
            if request[2] == MSG_TERMINATE:
                self.stop()
                continue
            self.socket_worker.send_multipart(request[:2] + self.get_payload(request[2:]))
        self.socket_worker.close()

    def get_payload(self, request):
        raise NotImplementedError()

    def stop(self):
        self.running = False


class BalancedServer:
    running = False

    def __init__(self, host, port, workers_count=5, worker_class=Worker):
        self.zmq_context = zmq.Context.instance()
        self.host = host
        self.port = port
        self.socket_frontend = None
        self.socket_backend = None
        self.port_backend = None
        self.workers_count = workers_count
        self.worker_class = worker_class

    def _init_frontend(self):
        self.socket_frontend = self.zmq_context.socket(zmq.ROUTER)
        self.socket_frontend.setsockopt(zmq.IDENTITY, "FE@{}:{}".format(self.host, self.port).encode())
        self.socket_frontend.bind("tcp://{}:{}".format(self.host, self.port))

    def _init_backend(self):
        self.socket_backend = self.zmq_context.socket(zmq.ROUTER)
        self.socket_backend.setsockopt(zmq.IDENTITY, "BE@{}:{}".format(self.host, self.port).encode())
        self.port_backend = self.socket_backend.bind_to_random_port("tcp://{}".format(self.host))

    def _init_workers(self):
        for i in range(self.workers_count):
            worker = self.worker_class("W_{}".format(i), self.host, self.port_backend, self.zmq_context)
            self.local_workers.append(worker)
            worker.start()

    def run(self):
        self.running = True
        self.registered_workers = {}
        self.local_workers = []
        self._init_frontend()
        self._init_backend()
        self.poller = zmq.Poller()
        self.poller.register(self.socket_backend, zmq.POLLIN)
        self.idle_workers = []
        self._init_workers()
        self.main_loop()

        self.socket_backend.close()
        self.socket_frontend.close()

    def main_loop(self):
        while self.running:
            sockets = dict(self.poller.poll(timeout=10))

            if self.socket_backend in sockets:
                # Handle worker activity on the backend
                request = self.socket_backend.recv_multipart()
                worker, _, client = request[:3]
                if not self.idle_workers:
                    # Poll for clients now that a worker is available
                    self.poller.register(self.socket_frontend, zmq.POLLIN)
                self.idle_workers.append(worker)

                if client != WORKER_READY:
                    # If client reply, send rest back to frontend
                    self.socket_frontend.send_multipart([client] + request[3:])
                else:
                    self.registered_workers[worker] = request[3:]

            if self.socket_frontend in sockets:
                # Get next client request, route to last-used worker
                request = self.socket_frontend.recv_multipart()

                worker = self.idle_workers.pop(0)
                instruction = request[2]
                self.socket_backend.send_multipart([worker, MSG_EMPTY] + request)
                if not self.idle_workers:
                    # Don't poll clients if no workers are available
                    self.poller.unregister(self.socket_frontend)

    def stop(self):
        for worker in self.local_workers:
            self.socket_backend.send_multipart([worker.id, MSG_EMPTY, MSG_EMPTY, MSG_EMPTY, MSG_TERMINATE])

        self.local_workers = []
        self.running = False

    def backend_address(self):
        return self.host, self.port_backend


class Publisher():
    running = False

    def __init__(self, host, port, zmq_context=None):
        self.zmq_context = zmq_context
        if self.zmq_context is None:
            self.zmq_context = zmq.Context.instance()
        self.host = host
        self.port = port
        self.publisher_events = {}
        self.messages_queue = deque()
        self._init_socket()

    def _init_socket(self):
        self.socket_publisher = zmq.Context.instance().socket(zmq.PUB)
        self.socket_publisher.setsockopt(zmq.IDENTITY, b"P_0")
        self.socket_publisher.bind("tcp://{}:{}".format(self.host, self.port))

    def run(self):
        timeout = 0.005
        self.running = True
        while self.running:
            publish_time = perf_counter_ns()
            while self.messages_queue:
                header, message, min_timeout = self.messages_queue.popleft()
                last_message_event = self.publisher_events.get(header, None)
                if (last_message_event is None) or (publish_time - last_message_event[0]) >= min_timeout:
                    self._publish_message(header, message)
                    self.publisher_events[header] = [publish_time, [header, None, min_timeout]]
                else:
                    last_message_event[1][1] = message

            for event in list(self.publisher_events.values()):
                if (publish_time - event[0]) >= event[1][2]:
                    if event[1][1] is not None:
                        self._publish_message(event[1][0], event[1][1])
                        self.publisher_events[event[1][0]] = [publish_time, [event[1][0], None, event[1][2]]]
                    else:
                        del self.publisher_events[event[1][0]]

            elapsed_ns = (perf_counter_ns() - publish_time) * 1e-9
            sleep_timeout = timeout - elapsed_ns
            sleep(sleep_timeout if sleep_timeout > 0 else 0)

    def _publish_message(self, header, message):
        raise NotImplementedError()

    def push_message(self, header, message, token=None, min_timeout=100e6):
        try:
            if token is not None:
                header += u"." + str(token)
            self.messages_queue.append((header, message, min_timeout))
        except TypeError:
            self.logger.exception(u"Error pushing message to client")

    def stop(self):
        self.running = False
