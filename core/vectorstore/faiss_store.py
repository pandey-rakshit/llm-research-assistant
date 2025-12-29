from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document as LCDocument

from core.embeddings.huggingface import HuggingFaceEmbeddingProvider
from core.models.document import DocumentChunk
from core.vectorstore.base import BaseVectorStore


class FAISSVectorStore(BaseVectorStore):
    def __init__(self, embedding_provider: HuggingFaceEmbeddingProvider):
        self.embedding_provider = embedding_provider
        self.store: FAISS | None = None

    def add(self, chunks: List[DocumentChunk]) -> None:
        docs = [
            LCDocument(
                page_content=c.content,
                metadata={
                    "document_id": c.document_id,
                    "chunk_id": c.chunk_id,
                    **c.metadata,
                },
            )
            for c in chunks
        ]

        if self.store is None:
            self.store = FAISS.from_documents(
                docs,
                embedding=self.embedding_provider.model,  # ✅ FIX
            )
        else:
            self.store.add_documents(docs)

    def search(self, query: str, top_k: int):
        docs = self.store.similarity_search(query, k=top_k)
        return [
            DocumentChunk(
                document_id=d.metadata["document_id"],
                chunk_id=d.metadata["chunk_id"],
                content=d.page_content,
                metadata=d.metadata,
            )
            for d in docs
        ]
