from pathlib import Path
import markdown
from bs4 import BeautifulSoup

from app.ingestion.document import Document


class MarkdownLoader:

    @staticmethod
    def load(file_path: str) -> Document:

        path = Path(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        html = markdown.markdown(md_text)

        soup = BeautifulSoup(html, "html.parser")

        content = soup.get_text(separator="\n")

        metadata = {
            "source": str(path),
            "file_name": path.name,
            "file_type": "md"
        }

        return Document(
            content=content,
            metadata=metadata
        )