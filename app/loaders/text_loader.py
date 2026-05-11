from app.chunking.document import Document


class TextLoader:

    @staticmethod
    def load(file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            text = f.read()

        return Document(
            text=text,
            metadata={
                "source": str(file_path),
                "file_name": file_path.split("/")[-1],
                "file_type": "txt"
            }
        )