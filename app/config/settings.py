from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CHROMA_DIR = DATA_DIR / "chroma_db"

# =========================
# MODELS
# =========================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

OLLAMA_MODEL = "mistral"

# =========================
# CHUNKING
# =========================

CHUNK_SIZE = 900
CHUNK_OVERLAP = 180

# =========================
# RETRIEVAL
# =========================

TOP_K_SEMANTIC = 10

TOP_K_BM25 = 10

TOP_K_RERANK = 3

# =========================
# PERFORMANCE
# =========================

ENABLE_RERANKING = True

SHOW_DEBUG_TIMINGS = True

MAX_CONTEXT_CHARS = 2500