from rich.console import Console

from app.embeddings.embedder import Embedder
from app.embeddings.vector_store import VectorStore

console = Console()


def main():

    query = "session fixation"

    embedder = Embedder()

    vector_store = VectorStore()

    query_embedding = embedder.embed_query(query)

    results = vector_store.search(
        query_embedding,
        top_k=3
    )

    console.print(
        "\n[bold green]SEARCH RESULTS[/bold green]\n"
    )

    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):

        console.print("=" * 80)

        console.print(f"Distance: {distance}")

        console.print(metadata)

        console.print("\n")

        console.print(doc)

        console.print("\n")


if __name__ == "__main__":
    main()