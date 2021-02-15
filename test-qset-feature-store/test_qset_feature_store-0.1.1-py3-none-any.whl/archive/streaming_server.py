from utils_ak.interactive_imports import *
from qset_feature_store.interactive_imports import *


configure_logging(stream=True, stream_level=logging.DEBUG)


class StreamingServer(ProductionMicroservice):
    def __init__(self):
        super().__init__()
        self.engines = []
        self.add_timer(self.process_engines, 1.0)  # try to close windows every one second
        self.add_callback('datasets', 'streaming', self.on_dataset)
        self.add_callback('feed', '', self.on_dataset_feed)

    def on_dataset(self, topic, msg):
        print('On dataset', topic, msg)
        dataset = msg
        engine = StreamingEngine(dataset)
        self.engines.append(engine)

    def on_dataset_feed(self, topic, msg):
        print('adding', msg['ts'], msg)
        for engine in self.engines:
            engine.add(msg['ts'], msg)

    def process_engines(self):
        # print('Processing engines', len(self.engines))
        for engine in self.engines:
            engine.process()


class Ping(ProductionMicroservice):
    def __init__(self, *args, **kwargs):
        super().__init__('Ping microservice', *args, **kwargs)

    def send_ping(self, topic, msg):
        self.logger.info(f'Received {topic} {msg}')
        cur_dt = cast_dt('2020.10.01 00:00:00')

        # time.sleep(3)
        # self.publish_json('datasets', 'streaming', get_sample_streaming_dataset())

        time.sleep(3)

        while True:
            self.publish_json('feed', '', {'ts': str(cur_dt), 'dataset': 'timebars', 'row': {'ticker': 'XTZ-USDT', 'pHigh': random.uniform(2.2, 2.4), 'pLow': random.uniform(2.0, 2.2)}})
            self.publish_json('feed', '', {'ts': str(cur_dt), 'dataset': 'timebars', 'row': {'ticker': 'BTC-USDT', 'pHigh': random.uniform(2.2, 2.4), 'pLow': random.uniform(2.0, 2.2)}})
            time.sleep(3)
            cur_dt += timedelta(minutes=10)


def run_ping():
    ping = Ping()

    async def send_initial():
        await asyncio.sleep(1.0)
        ping.send_ping('init', 'init')

    ping.tasks.append(asyncio.ensure_future(send_initial()))
    ping.run()


if __name__ == '__main__':
    multiprocessing.Process(target=run_ping).start()
    server = StreamingServer()
    # run_listener_async('heartbeat', brokers_config=server.brokers_config)
    server.run()

