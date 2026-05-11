from pypdf import PdfReader

from app.chunking.document import Document


class PDFLoader:

    @staticmethod
    def load(file_path):

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted + "\n"

        return Document(
            text=text,
            metadata={
                "source": str(file_path),
                "file_name": file_path.split("/")[-1],
                "file_type": "pdf"
            }
        )