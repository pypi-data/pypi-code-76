import asyncio
from utils_ak.mongo_job_queue.worker.worker import Worker
from utils_ak.mongo_job_queue.worker.worker_test import *

# from qset_feature_store import qdm, QsetRepositoryClient


class DatasetWorker(Worker):
    def __init__(self, *args, **kwargs):
        # todo: use secrets
        super().__init__(*args, **kwargs)
        # self.cli = QsetRepositoryClient('akadaner', host='mongodb+srv://arseniikadaner:Nash0lsapog@cluster0.2umoy.mongodb.net/feature-store?retryWrites=true&w=majority')

    async def process(self):
        # fs = self.cli.get(id=self.payload['featureset_id'])

        # self.microservice.logger.info('Calculating featureset', featureset_id=fs['_id'])
        self.microservice.logger.info('Calculating featureset', featureset_id=self.payload['featureset_id'])

        # todo: switch-com
        # df = qdm.get_dataset(fs)
        time.sleep(5)

        # todo: save dataset to output storage (clickhouse)

        # todo: switch-com
        # self.microservice.send_state('success', {'calculated_length': len(df)})

        # self.microservice.logger.info('Successfully calculated featureset', featureset_id=fs['_id'])
        self.microservice.logger.info('Successfully calculated featureset', featureset_id=self.payload['featureset_id'])
        self.microservice.send_state('success', {'calculated_length': 78078})


def test_batch():
    test_worker(DatasetWorker, {'featureset_id': '602020f1079228082591d0cf'}, message_broker=('zmq', {'endpoints': {'monitor': {'endpoint': 'tcp://localhost:5555', 'type': 'sub'}}}))


def test_streaming():
    test_worker(DatasetWorker, {'featureset_id': '602020f1079228082591d0cf'}, message_broker=('zmq', {'endpoints': {'monitor': {'endpoint': 'tcp://localhost:5555', 'type': 'sub'}}}))


def test_deployment():
    test_worker_deployment('deployment.yml', message_broker=('zmq', {'endpoints': {'monitor': {'endpoint': 'tcp://localhost:5555', 'type': 'sub'}}}))


if __name__ == '__main__':
    # test_batch()
    # test_streaming()
    test_deployment()