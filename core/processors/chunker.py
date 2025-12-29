import uuid
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings
from core.models.document import DocumentChunk, DocumentSection


class DocumentChunker:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )

    def chunk(self, sections: List[DocumentSection]) -> List[DocumentChunk]:
        chunks = []
        for section in sections:
            texts = self.splitter.split_text(section.content)
            for idx, text in enumerate(texts):
                chunks.append(
                    DocumentChunk(
                        document_id=section.document_id,
                        chunk_id=str(uuid.uuid4()),
                        content=text,
                        metadata={
                            **section.metadata,
                            "section": section.section_name,
                            "chunk_index": idx,
                        },
                    )
                )
        return chunks
