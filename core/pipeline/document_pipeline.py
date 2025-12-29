import pprint
from typing import List

from core.loaders.base import BaseDocumentLoader
from core.models.document import DocumentChunk
from core.processors.chunker import DocumentChunker
from core.processors.section_extractor import SectionExtractor


class DocumentIngestionPipeline:
    def __init__(
        self,
        loader: BaseDocumentLoader,
        extractor: SectionExtractor,
        chunker: DocumentChunker,
    ):
        self.loader = loader
        self.extractor = extractor
        self.chunker = chunker

    def ingest(self, path: str) -> List[DocumentChunk]:
        documents = self.loader.load(path)
        chunks: List[DocumentChunk] = []

        metadata = documents[0].metadata if documents else {}
        pprint.pprint(metadata, indent=4)

        for doc in documents:
            sections = self.extractor.extract(doc)
            chunks.extend(self.chunker.chunk(sections))

        return chunks, metadata
