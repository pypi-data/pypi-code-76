class Embedder:

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def get_embeddings(self, sentences, do_write=False):
        embeddings = self.embedding_model(sentences)
        return embeddings.numpy()
