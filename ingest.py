from rich.console import Console

from app.ingestion.ingest import IngestionPipeline
from app.chunking.smart_chunker import SmartChunker

from app.embeddings.embedder import Embedder
from app.embeddings.vector_store import VectorStore

console = Console()


def main():

    file_path = "data/raw/sample.pdf"

    console.print("\n[bold green]INGESTION STARTED[/bold green]\n")

    # Load document
    document = IngestionPipeline.ingest(file_path)

    # Chunking
    chunks = SmartChunker.chunk(document)

    console.print(f"TOTAL CHUNKS: {len(chunks)}\n")

    # Embeddings
    texts = [chunk.text for chunk in chunks]

    embedder = Embedder()

    embeddings = embedder.embed_texts(texts)

    console.print(
        f"EMBEDDINGS CREATED: {len(embeddings)}\n"
    )

    # Store
    vector_store = VectorStore()

    vector_store.add_chunks(
        chunks,
        embeddings
    )

    console.print(
        "\n[bold green]INGESTION COMPLETE[/bold green]\n"
    )


if __name__ == "__main__":
    main()