from pathlib import Path

from app.ingestion.document import Document


class TXTLoader:

    @staticmethod
    def load(file_path: str) -> Document:

        path = Path(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        metadata = {
            "source": str(path),
            "file_name": path.name,
            "file_type": "txt"
        }

        return Document(
            content=content,
            metadata=metadata
        )