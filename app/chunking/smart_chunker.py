from typing import List

from app.chunking.chunk import Chunk
from app.chunking.splitter import SmartSplitter


class SmartChunker:

    @staticmethod
    def chunk(document) -> List[Chunk]:

        splitter = SmartSplitter.get_splitter()

        split_texts = splitter.split_text(document.text)

        chunks = []

        for index, text in enumerate(split_texts):

            metadata = document.metadata.copy()

            metadata.update({
                "chunk_id": index
            })

            chunks.append(
                Chunk(
                    text=text,
                    metadata=metadata
                )
            )

        return chunks