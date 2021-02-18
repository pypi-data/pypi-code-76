from utils_ak.loguru import *

from qset_feature_store import *
from qset_feature_store.dataset_manager.dataset_manager import qdm
from qset_feature_store.repository import QsetRepositoryClient


CLI = QsetRepositoryClient('akadaner')


class HistoricalServer(ProductionMicroservice):
    def __init__(self):
        super().__init__()
        self.add_callback('datasets', 'historical', self.on_dataset)

    def on_dataset(self, topic, msg):
        featureset = CLI.get(_id=cast_object_id(msg['featureset']['_id']))
        print(qdm.get_dataset(featureset))


class Ping(ProductionMicroservice):
    def __init__(self, *args, **kwargs):
        super().__init__('Ping microservice', *args, **kwargs)

    def send_ping(self, topic, msg):
        self.logger.info(f'Received {topic} {msg}')
        time.sleep(3)


def run_ping():
    ping = Ping()

    async def send_initial():
        await asyncio.sleep(3.0)
        try:
            ping.publish_json('datasets', 'historical', {'featureset': {'_id': str(CLI.get_latest(user='akadaner', name='timebars')['_id'])}})
        except Exception as e:
            import traceback
            traceback.print_exc()
            print('hey')
        # ping.publish_json('datasets', 'historical', {})
        print('sent')

    ping.tasks.append(asyncio.ensure_future(send_initial()))
    ping.run()


if __name__ == '__main__':
    multiprocessing.Process(target=run_ping).start()
    server = HistoricalServer()
    # run_listener_async('heartbeat', brokers_config=server.brokers_config)
    server.run()
