from app.ingestion.factory import LoaderFactory


class IngestionPipeline:

    @staticmethod
    def ingest(file_path):

        loader = LoaderFactory.get_loader(
            file_path
        )

        document = loader.load(
            file_path
        )

        return document