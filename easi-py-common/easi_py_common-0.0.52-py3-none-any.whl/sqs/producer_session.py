from gevent.pool import Pool

pool = Pool(64)


class ProducerSession:
    buffer_size = 10

    def __init__(self, sqs_client, sign, app=None, cb=None):
        self.sqs_client = sqs_client
        self.sign = sign
        self.app = app
        self.cb = cb
        self.msgs = []

    def add(self, address, msg, key='', group_id='', delay_seconds=0, sign=None):
        if sign is None:
            address = self.sign + address
        else:
            address = sign + address

        self.msgs.append(dict(
            address=address,
            body=msg,
            key=key,
            group_id=group_id,
            delay_seconds=delay_seconds
        ))

    def flush(self):
        self.msgs = []

    def commit(self):
        if not self.msgs:
            return
        temp_msgs = self.msgs[:]
        self.msgs = []
        msg_group_map = {}

        for msg in temp_msgs:
            if msg.address not in msg_group_map:
                msg_group_map[msg.address] = []
            msg_group_map[msg.address].append(msg)
        for address, msg_list in msg_group_map.items():
            msg_buffer_list = []
            for m in msg_list:
                msg_buffer_list.append(m)
                if len(msg_buffer_list) % self.buffer_size == 0:
                    pool.spawn(self.sqs_client.send_message_batch, address, msg_buffer_list, cb=self.cb, app=self.app)
                    msg_buffer_list = []
            if msg_buffer_list:
                pool.spawn(self.sqs_client.send_message_batch, msg_buffer_list, cb=self.cb, app=self.app)
