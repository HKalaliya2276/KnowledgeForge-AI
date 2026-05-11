from rich.console import Console
from rich.prompt import Prompt

import time

from app.embeddings.embedder import Embedder
from app.embeddings.vector_store import VectorStore

from app.chunking.chunk import Chunk

from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.hybrid_retriever import HybridRetriever

from app.reranker.reranker import Reranker

from app.llm.ollama_client import OllamaClient

from app.config.settings import (
    TOP_K_SEMANTIC,
    TOP_K_BM25,
    TOP_K_RERANK,
    ENABLE_RERANKING,
    SHOW_DEBUG_TIMINGS,
    MAX_CONTEXT_CHARS
)

console = Console()


def retrieve_context(
    query,
    embedder,
    vector_store,
    reranker
):

    start_time = time.time()

    # =========================
    # QUERY EMBEDDING
    # =========================

    query_embedding = embedder.embed_query(query)

    if SHOW_DEBUG_TIMINGS:

        console.print(
            f"[cyan]Query Embedding:[/cyan] "
            f"{time.time() - start_time:.2f}s"
        )

    # =========================
    # SEMANTIC SEARCH
    # =========================

    semantic_results = vector_store.search(
        query_embedding,
        top_k=TOP_K_SEMANTIC
    )

    if SHOW_DEBUG_TIMINGS:

        console.print(
            f"[cyan]Semantic Retrieval:[/cyan] "
            f"{time.time() - start_time:.2f}s"
        )

    # =========================
    # CONVERT TO CHUNKS
    # =========================

    chunks = []

    for doc, metadata in zip(
        semantic_results["documents"][0],
        semantic_results["metadatas"][0]
    ):

        chunks.append(
            Chunk(
                text=doc,
                metadata=metadata
            )
        )

    # =========================
    # BM25
    # =========================

    bm25 = BM25Retriever()

    bm25.build_index(chunks)

    bm25_results = bm25.search(
        query,
        top_k=TOP_K_BM25
    )

    if SHOW_DEBUG_TIMINGS:

        console.print(
            f"[cyan]BM25:[/cyan] "
            f"{time.time() - start_time:.2f}s"
        )

    # =========================
    # HYBRID MERGE
    # =========================

    hybrid_results = HybridRetriever.merge_results(
        semantic_results,
        bm25_results
    )

    # =========================
    # RERANKING
    # =========================

    if ENABLE_RERANKING:

        final_results = reranker.rerank(
            query,
            hybrid_results,
            top_k=TOP_K_RERANK
        )

    else:

        final_results = hybrid_results[:TOP_K_RERANK]

    if SHOW_DEBUG_TIMINGS:

        console.print(
            f"[cyan]Reranking:[/cyan] "
            f"{time.time() - start_time:.2f}s"
        )

    # =========================
    # CONTEXT BUILD
    # =========================

    context = "\n\n".join(
        result["text"]
        for result in final_results
    )

    # LIMIT CONTEXT SIZE
    context = context[:MAX_CONTEXT_CHARS]

    if SHOW_DEBUG_TIMINGS:

        console.print(
            f"[bold magenta]Total Retrieval:[/bold magenta] "
            f"{time.time() - start_time:.2f}s\n"
        )

    return context


def main():

    console.print(
        "\n[bold green]CYBERSEC RAG ASSISTANT[/bold green]\n"
    )

    console.print(
        "[bold yellow]Loading models...[/bold yellow]\n"
    )

    model_load_start = time.time()

    # LOAD ONCE
    embedder = Embedder()

    reranker = Reranker()

    vector_store = VectorStore()

    console.print(
        f"[bold green]System Ready "
        f"({time.time() - model_load_start:.2f}s)[/bold green]\n"
    )

    while True:

        query = Prompt.ask(
            "\n[bold cyan]You[/bold cyan]"
        )

        if query.lower() in ["exit", "quit"]:

            console.print(
                "\n[bold red]Goodbye[/bold red]\n"
            )

            break

        # =========================
        # RETRIEVAL
        # =========================

        context = retrieve_context(
            query,
            embedder,
            vector_store,
            reranker
        )

        console.print(
            "\n[bold yellow]Generating answer...[/bold yellow]\n"
        )

        # =========================
        # GENERATION
        # =========================

        console.print(
            f"[blue]Context Length:[/blue] "
            f"{len(context)} chars"
        )

        generation_start = time.time()

        answer = OllamaClient.generate(
            query,
            context
        )

        generation_time = (
            time.time() - generation_start
        )

        console.print(
            f"[bold magenta]Generation Time:[/bold magenta] "
            f"{generation_time:.2f}s\n"
        )

        # =========================
        # OUTPUT
        # =========================

        console.print(
            "\n[bold green]Assistant[/bold green]\n"
        )

        console.print(answer)


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        console.print(
            "\n\n[bold yellow]Shutdown Requested[/bold yellow]"
        )

        console.print(
            "[bold red]CyberSec RAG Assistant Closed[/bold red]\n"
        )

    except Exception as e:

        console.print(
            f"\n[bold red]Fatal Error:[/bold red] {e}\n"
        )