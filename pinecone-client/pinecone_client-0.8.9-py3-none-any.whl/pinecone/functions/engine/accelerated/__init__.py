from pinecone.functions.engine.namespaced import NamespacedEngine


class AcceleratedEngine(NamespacedEngine):

    @property
    def cpu_request(self):
        return 2000
