from sentence_transformers import SentenceTransformer

from app.config.settings import EMBEDDING_MODEL


class Embedder:

    _model = None

    def __init__(self):

        if Embedder._model is None:

            print("\nLOADING EMBEDDING MODEL...\n")

            Embedder._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

        self.model = Embedder._model

    def embed_texts(self, texts):

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    def embed_query(self, query):

        embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        return embedding.tolist()