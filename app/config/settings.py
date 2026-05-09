from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CHROMA_DIR = DATA_DIR / "chroma_db"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

RERANK_MODEL = "BAAI/bge-reranker-base"

OLLAMA_MODEL = "mistral"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 180

TOP_K_RETRIEVAL = 10
TOP_K_RERANK = 5