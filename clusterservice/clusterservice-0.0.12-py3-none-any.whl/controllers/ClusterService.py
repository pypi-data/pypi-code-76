import logging
import os
import traceback
from typing import List

import bentoml
from bentoml.adapters import JsonInput
from bentoml import BentoService
from bentoml.types import InferenceTask, JsonSerializable
from qandaxfmrartifact.QandaTransformersModelArtifact import QandaTransformersModelArtifact
from tfhubartifact.TensorFlowHubModelArtifact import TensorFlowHubModelArtifact

from clusterservice.services.GraphDbReaderWriter import GraphDbReaderWriter
from clusterservice.services.Neo4jDatabase import Neo4jDatabase

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


@bentoml.env(
    docker_base_image='markmo/clusterservice-base:0.0.3',
    pip_packages=[  # also installed in base image
        'neo4j==4.2.1',
        'neomodel==4.0.1',
        'nmslib==2.0.8',
        'pandas==1.1.5',
        'qandaxfmrartifact==0.0.9',
        'scikit-learn==0.23.2',
        'spacy==2.3.5',
        'tensorflow==2.0.0',
        'tensorflow-hub==0.5.0',
        'tfhubartifact==0.0.5',
        'tokenizers==0.7.0',
        'transformers==2.10.0',
        'wheel==0.36.2',
    ],
)
@bentoml.artifacts([
    QandaTransformersModelArtifact('albert'),
    TensorFlowHubModelArtifact('embedder'),
])
class ClusterService(BentoService):

    def __init__(self):
        super(ClusterService, self).__init__()
        self.db = None
        self.db_reader_writer = None

    @bentoml.api(input=JsonInput(), batch=True)
    def predict(self, parsed_json_list: List[JsonSerializable], tasks: List[InferenceTask]):
        logger.info('GET /predict')

        if self.db is None:
            self.db = Neo4jDatabase(
                host=os.environ['NEO4J_HOST'],
                username=os.environ['NEO4J_USERNAME'],
                password=os.environ['NEO4J_PASSWORD'],
            )

        if self.db_reader_writer is None:
            self.db_reader_writer = GraphDbReaderWriter(self.db)

        results = []
        for item, task in zip(parsed_json_list, tasks):
            if ('question_texts' not in item or
                'forum_id' not in item):
                task.discard(http_status=500, err_msg='Invalid input')

            try:
                result = self.db_reader_writer.get_from_db(
                    question_texts=item['question_texts'],
                    forum_id=item['forum_id'],
                )
                results.append(result)

            except Exception as err:  # noqa
                err_msg = 'Inference failed with valid input: {}'.format(err)
                logger.error(err_msg)
                traceback.print_exc()
                task.discard(http_status=500, err_msg=err_msg)

        return results
