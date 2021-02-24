from asyncio import iscoroutinefunction


class message():
    '''class for sending messages'''

    adresses = {} # {adr: fn}
    messages = [] # [(adr, mes_id, mes_data), (...)]


    @classmethod
    def update(message):
        while len(message.messages) > 0:
            msg = message.messages.pop(0)
            adr, msg_id, msg_data = msg[0], msg[1], msg[2]

            subscriber = message.adresses.get(adr)
            if subscriber is not None:
                subscriber(msg_id, msg_data)

    @classmethod
    def async_update(message, loop):
        while len(message.messages) > 0:
            msg = message.messages.pop(0)
            adr, msg_id, msg_data = msg[0], msg[1], msg[2]

            subscriber = message.adresses.get(adr)
            if subscriber is not None:
                if iscoroutinefunction(subscriber):
                    loop.create_task(subscriber(msg_id, msg_data))

                else:
                    subscriber = message.create_async_func(subscriber)
                    loop.create_task(subscriber(msg_id, msg_data))


    @classmethod
    def subscribe(message, adress, fn):
        message.adresses[adress] = fn

    @classmethod
    def unsubscribe(message, adress):
        if adress in message.adresses.keys():
            del message.adresses[adress]


    @classmethod
    def post(message, adress, message_id, message_data=None):
        message.messages.append((adress, message_id, message_data))


    @staticmethod
    def create_async_func(func):
        async def async_func(msg_id, msg_data):
            func(msg_id, msg_data)
        return async_func
