from sentence_transformers import CrossEncoder

from app.config.settings import RERANK_MODEL


class Reranker:

    _model = None

    def __init__(self):

        if Reranker._model is None:

            print("\nLOADING RERANKER MODEL...\n")

            Reranker._model = CrossEncoder(
                RERANK_MODEL
            )

        self.model = Reranker._model

    def rerank(
        self,
        query,
        results,
        top_k=5
    ):

        pairs = [
            (query, result["text"])
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked = []

        for result, score in zip(results, scores):

            result["rerank_score"] = float(score)

            reranked.append(result)

        reranked.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked[:top_k]