class HybridRetriever:

    @staticmethod
    def merge_results(
        semantic_results,
        bm25_results,
        alpha=0.7
    ):

        combined = {}

        # Semantic Results
        semantic_docs = semantic_results["documents"][0]
        semantic_meta = semantic_results["metadatas"][0]
        semantic_dist = semantic_results["distances"][0]

        # Normalize semantic scores
        max_dist = max(semantic_dist) if semantic_dist else 1

        for doc, metadata, distance in zip(
            semantic_docs,
            semantic_meta,
            semantic_dist
        ):

            key = metadata["chunk_id"]

            semantic_score = 1 - (distance / max_dist)

            combined[key] = {
                "text": doc,
                "metadata": metadata,
                "semantic_score": semantic_score,
                "bm25_score": 0.0
            }

        # BM25 normalization
        if bm25_results:

            max_bm25 = max(score for _, score in bm25_results)

            if max_bm25 == 0:
                max_bm25 = 1

            for chunk, bm25_score in bm25_results:

                key = chunk.metadata["chunk_id"]

                normalized_bm25 = bm25_score / max_bm25

                if key in combined:

                    combined[key]["bm25_score"] = normalized_bm25

                else:

                    combined[key] = {
                        "text": chunk.text,
                        "metadata": chunk.metadata,
                        "semantic_score": 0.0,
                        "bm25_score": normalized_bm25
                    }

        # Final Weighted Score
        final_results = []

        for item in combined.values():

            final_score = (
                alpha * item["semantic_score"]
                +
                (1 - alpha) * item["bm25_score"]
            )

            item["final_score"] = final_score

            final_results.append(item)

        final_results.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        return final_results