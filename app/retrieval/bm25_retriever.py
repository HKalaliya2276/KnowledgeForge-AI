from rank_bm25 import BM25Okapi

from app.retrieval.tokenizer import SimpleTokenizer


class BM25Retriever:

    def __init__(self):

        self.bm25 = None

        self.chunks = []

    def build_index(self, chunks):

        self.chunks = chunks

        tokenized_chunks = [
            SimpleTokenizer.tokenize(chunk.text)
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def search(self, query, top_k=5):

        tokenized_query = SimpleTokenizer.tokenize(query)

        scores = self.bm25.get_scores(tokenized_query)

        scored_chunks = list(zip(self.chunks, scores))

        scored_chunks.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return scored_chunks[:top_k]