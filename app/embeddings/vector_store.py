import chromadb

from app.config.settings import CHROMA_DIR


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        self.collection = self.client.get_or_create_collection(
            name="cybersec_rag"
        )

    def add_chunks(self, chunks, embeddings):

        ids = []

        documents = []

        metadatas = []

        for i, chunk in enumerate(chunks):

            source_name = chunk.metadata["file_name"]
            chunk_id = chunk.metadata["chunk_id"]
            ids.append(f"{source_name}_{chunk_id}")

            documents.append(chunk.text)

            metadatas.append(chunk.metadata)

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query_embedding, top_k=5):

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results