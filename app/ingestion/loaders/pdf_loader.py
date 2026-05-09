from pathlib import Path
from pypdf import PdfReader

from app.ingestion.document import Document


class PDFLoader:

    @staticmethod
    def load(file_path: str) -> Document:

        path = Path(file_path)

        reader = PdfReader(file_path)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        content = "\n".join(text)

        metadata = {
            "source": str(path),
            "file_name": path.name,
            "file_type": "pdf"
        }

        return Document(
            content=content,
            metadata=metadata
        )