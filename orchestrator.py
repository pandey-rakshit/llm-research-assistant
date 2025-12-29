from core.pipeline.document_pipeline import DocumentIngestionPipeline
from core.vectorstore.base import BaseVectorStore


class KnowledgeBaseOrchestrator:
    def __init__(
        self,
        pipeline: DocumentIngestionPipeline,
        store: BaseVectorStore,
    ):
        self.pipeline = pipeline
        self.store = store

    def ingest(self, path: str):
        chunks, metadata = self.pipeline.ingest(path)
        self.store.add(chunks)
        return metadata
