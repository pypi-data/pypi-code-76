import fire
from functools import partial
from utils_ak.mongo_job_queue.worker.worker import *
from qset_feature_store.worker.dataset.dataset_worker import DatasetWorker

if __name__ == '__main__':
    fire.Fire(partial(run_worker, worker_cls=DatasetWorker))
