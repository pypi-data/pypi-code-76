#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions.engine import Engine
from pinecone.protos import core_pb2
from pydoc import locate


class NamespacedEngine(Engine):
    """
    This engine allows indexing of vectors in namespaces using exact or approximated engines, such that
    each namespace will is handled by a unique sub-engine.
    """

    SUPPORTED_ENGINES = {'approximated': 'pinecone_engine.functions.engine.approximated.ApproximatedEngine',
                         'exact': 'pinecone_engine.functions.engine.exact.ExactEngine',
                         'exactly': 'pinecone_engine.functions.engine.exact.ExactlyEngine'}
    SUPPORTED_ENGINE_IMAGES = {'approximated': 'pinecone/engine/approximated',
                               'exact': 'pinecone/engine/exact',
                               'exactly': 'pinecone/engine/exactly'}

    @property
    def image(self):
        return self.SUPPORTED_ENGINE_IMAGES[self.config['engine_type']]

    def __init__(self, engine_type="approximated", *args,  **config):
        """
        NamespacedEngine Constructor
        :param engine_type: type of engine to use for each namespace.
                            The supported engines are 'approximated' and 'exact':
                            'approximated' -  This engine allows a fast approximated search based on common metrics
                                              It's based on Pinecone's proprietary vector index
                            'exact' -  This engine allows an accurate vector search based on common metrics
                                       It's based on an exhaustive search, thus might be slow
        :param metric: type of metric used in the vector index -
                        'cosine' - cosine similarity
                        'dotproduct' - dot-product
                        'euclidean' - euclidean distance
        :return:
        """
        super().__init__(*args, **config)
        self.config['engine_type'] = engine_type
        self.engine_class = None
        self.engines = {}

    def setup(self):
        super().setup()
        self.engine_class = self.get_engine_class()

    def cleanup(self):
        for engine in self.engines.values():
            engine.cleanup()

    def get_engine_class(self):
        engine_type = self.config['engine_type']
        if engine_type not in NamespacedEngine.SUPPORTED_ENGINES:
            raise ValueError(f'{engine_type} is not a supported engine type')
        return locate(NamespacedEngine.SUPPORTED_ENGINES[engine_type])

    def handle_msg(self, msg: 'core_pb2.Request') -> 'core_pb2.Request':
        namespace = msg.namespace
        req_type = msg.WhichOneof('body')
        if req_type == 'index':
            if namespace not in self.engines:
                engine_name = f'{self.name}-{self.id}-{namespace}'
                new_engine = self.engine_class(name=engine_name, **self.config)
                new_engine.setup()
                self.engines[namespace] = new_engine
            msg = self.engines[namespace].handle_msg(msg)
        else:
            if namespace not in self.engines:
                return msg
            else:
                relevant_engines = [self.engines[namespace]]
            for engine in relevant_engines:
                msg = engine.handle_msg(msg)
        return msg

    def size(self) -> int:
        return sum(engine.size() for engine in self.engines.values())
