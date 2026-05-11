from pathlib import Path

from app.loaders.pdf_loader import PDFLoader
from app.loaders.text_loader import TextLoader
from app.loaders.docx_loader import DocxLoader
from app.loaders.markdown_loader import MarkdownLoader


class LoaderFactory:

    @staticmethod
    def get_loader(file_path):

        extension = Path(
            file_path
        ).suffix.lower()

        loaders = {

            ".pdf": PDFLoader(),

            ".txt": TextLoader(),

            ".docx": DocxLoader(),

            ".md": MarkdownLoader()
        }

        if extension not in loaders:

            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return loaders[extension]