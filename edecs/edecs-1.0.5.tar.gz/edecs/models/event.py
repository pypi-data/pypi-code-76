from asyncio import iscoroutinefunction


class event():
    '''class for sending events'''

    events = [] # [(ev_type, ev_data), (ev_type, ev_data)]
    subscribers = {} # {event_type: [sub1, sub2, sub3]}
    subscribed_systems = {} # {sys_type: [(ev_type, fn), (...)]}


    @classmethod
    def update(event):
        while len(event.events) > 0:
            ev = event.events.pop(0)
            event_type, event_data = ev[0], ev[1]
            subscribers = event.subscribers.get('_all', []) + event.subscribers.get(event_type, [])

            for subscriber in subscribers:
                subscriber(event_type, event_data)

    @classmethod
    def async_update(event, loop):
        while len(event.events) > 0:
            ev = event.events.pop(0)
            event_type, event_data = ev[0], ev[1]
            subscribers = event.subscribers.get('_all', []) + event.subscribers.get(event_type, [])

            for subscriber in subscribers:
                if iscoroutinefunction(subscriber):
                    loop.create_task(subscriber(event_type, event_data))

                else:
                    subscriber = event.create_async_func(subscriber)
                    loop.create_task(subscriber(event_type, event_data))


    @classmethod
    def subscribe(event, system, event_type='_all', fn=None):
        if fn is None:
            fn = system.on_event

        if event.subscribers.get(event_type) is None:
            event.subscribers[event_type] = []

        if fn not in event.subscribers[event_type]:
            event.subscribers[event_type].append(fn)

            if event.subscribed_systems.get(system.type) is None:
                event.subscribed_systems[system.type] = []

            event.subscribed_systems[system.type].append((event_type, fn))

    @classmethod
    def unsubscribe(event, system, event_type='_all', fn=None):
        if fn is None:
            fn = system.on_event

        if event.subscribers.get(event_type) is None:
            return

        if fn not in event.subscribers[event_type]:
            return

        event.subscribers[event_type].remove(fn)

        if len(event.subscribers[event_type]) == 0:
            del event.subscribers[event_type]

        event.subscribed_systems[system.type].remove((event_type, fn))

        if len(event.subscribed_systems[system.type]) == 0:
            del event.subscribed_systems[system.type]

    @classmethod
    def unsubscribe_system(event, system):
        subscribed_events = event.subscribed_systems.get(system.type, []).copy()

        for sub_event in subscribed_events:
            ev_type, fn = sub_event[0], sub_event[1]

            event.unsubscribe(system, ev_type, fn)

    @classmethod
    def fire(event, event_type, event_data=None):
        event.events.append((event_type, event_data))


    @staticmethod
    def create_async_func(func):
        async def async_func(event_type, event_data):
            func(event_type, event_data)
        return async_func
