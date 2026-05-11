from rich.console import Console

from app.ingestion.ingest import IngestionPipeline
from app.ingestion.file_registry import FileRegistry
from app.ingestion.file_scanner import FileScanner

from app.chunking.smart_chunker import SmartChunker

from app.embeddings.embedder import Embedder
from app.embeddings.vector_store import VectorStore

from app.utils.hashing import FileHasher

from app.config.settings import RAW_DATA_DIR

console = Console()


def main():

    console.print(
        "\n[bold green]SMART INCREMENTAL INGESTION STARTED[/bold green]\n"
    )

    # =========================
    # REGISTRY
    # =========================

    registry = FileRegistry(
        "data/registry/processed_files.json"
    )

    # =========================
    # RECURSIVE FILE SCAN
    # =========================

    files = FileScanner.scan(
        RAW_DATA_DIR
    )

    console.print(
        f"[bold cyan]FILES FOUND:[/bold cyan] {len(files)}\n"
    )

    # =========================
    # LOAD MODELS ONCE
    # =========================

    embedder = Embedder()

    vector_store = VectorStore()

    # =========================
    # STATS
    # =========================

    new_files = 0

    skipped_files = 0

    duplicate_files = 0

    # =========================
    # PROCESS FILES
    # =========================

    for file_path in files:

        console.print(
            f"\n[cyan]CHECKING:[/cyan] {file_path}"
        )

        try:

            # =========================
            # LOAD DOCUMENT
            # =========================

            document = IngestionPipeline.ingest(
                str(file_path)
            )

            # =========================
            # CONTENT HASH
            # =========================

            content_hash = FileHasher.hash_text(
                document.text
            )

            # =========================
            # DUPLICATE CHECK
            # =========================

            if registry.is_hash_processed(
                content_hash
            ):

                console.print(
                    "[yellow]DUPLICATE CONTENT SKIPPED:[/yellow] "
                    f"{file_path}"
                )

                duplicate_files += 1

                continue

            console.print(
                f"[green]NEW CONTENT DETECTED[/green]"
            )

            # =========================
            # CHUNKING
            # =========================

            chunks = SmartChunker.chunk(
                document
            )

            console.print(
                f"Chunks Created: {len(chunks)}"
            )

            texts = [
                chunk.text
                for chunk in chunks
            ]

            # =========================
            # EMBEDDINGS
            # =========================

            embeddings = embedder.embed_texts(
                texts
            )

            console.print(
                f"Embeddings Created: {len(embeddings)}"
            )

            # =========================
            # VECTOR STORE
            # =========================

            vector_store.add_chunks(
                chunks,
                embeddings
            )

            # =========================
            # SAVE TO REGISTRY
            # =========================

            registry.add_file(
                file_path=file_path,
                content_hash=content_hash,
                chunk_count=len(chunks)
            )

            console.print(
                f"[bold green]SUCCESS:[/bold green] "
                f"{file_path}\n"
            )

            new_files += 1

        except Exception as e:

            console.print(
                f"[bold red]ERROR:[/bold red] {e}\n"
            )

    # =========================
    # FINAL STATS
    # =========================

    console.print(
        "\n[bold green]INGESTION COMPLETE[/bold green]\n"
    )

    console.print(
        f"[green]NEW FILES:[/green] {new_files}"
    )

    console.print(
        f"[yellow]DUPLICATES SKIPPED:[/yellow] "
        f"{duplicate_files}"
    )

    console.print(
        f"[cyan]TOTAL FILES SCANNED:[/cyan] "
        f"{len(files)}"
    )


if __name__ == "__main__":
    main()