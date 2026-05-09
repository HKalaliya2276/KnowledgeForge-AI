from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.loaders.docx_loader import DOCXLoader
from app.ingestion.loaders.txt_loader import TXTLoader
from app.ingestion.loaders.md_loader import MarkdownLoader


class LoaderFactory:

    LOADERS = {
        ".pdf": PDFLoader,
        ".docx": DOCXLoader,
        ".txt": TXTLoader,
        ".md": MarkdownLoader
    }

    @classmethod
    def get_loader(cls, extension: str):

        loader = cls.LOADERS.get(extension.lower())

        if not loader:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader