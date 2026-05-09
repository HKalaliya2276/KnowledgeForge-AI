from pathlib import Path

from app.ingestion.cleaner import TextCleaner
from app.ingestion.loaders.loader_factory import LoaderFactory


class IngestionPipeline:

    @staticmethod
    def ingest(file_path: str):

        path = Path(file_path)

        loader_class = LoaderFactory.get_loader(path.suffix)

        document = loader_class.load(file_path)

        cleaned_text = TextCleaner.clean(document.content)

        document.content = cleaned_text

        return document