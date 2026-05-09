from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


class SmartSplitter:

    @staticmethod
    def get_splitter():

        return RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,

            separators=[
                "\n# ",
                "\n## ",
                "\n### ",

                "\n```",
                "\n\n",

                "\n- ",
                "\n* ",

                "\n1. ",
                "\n2. ",

                "\n",

                ". ",

                " "
            ]
        )