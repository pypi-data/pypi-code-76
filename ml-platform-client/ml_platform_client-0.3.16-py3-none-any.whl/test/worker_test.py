from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection


def ping(conn):
    for i in range(3):
        conn.send('pong')
        msg = conn.recv()
        print(msg)
    conn.send('exit')


def pong(conn):
    while True:
        msg = conn.recv()
        if msg == 'exit':
            print('exit')
            return
        print(msg)
        conn.send('ping')


class Worker1(Process):
    def __init__(self, pipe: Connection):
        super(Worker1, self).__init__()
        self.pipe = pipe
        self.model_pool = {}
        self.alg_mapping = {}

    def run(self):
        try:
            while True:
                try:
                    command, data = self.pipe.recv()
                    if command == 'exit':
                        return
                    try:
                        result = command + ' success'
                    except Exception as e:
                        result = False, None

                    self.pipe.send(result)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    worker1 = Worker1(child_conn)
    worker1.start()
    parent_conn.send(('cmd1', []))
    parent_conn.send(('cmd2', []))
    parent_conn.send(('exit', []))
    print(parent_conn.recv())
    print(parent_conn.recv())
    print('over')
