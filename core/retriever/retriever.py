from typing import List

from core.models.document import DocumentChunk
from core.vectorstore.base import BaseVectorStore


class RetrieverService:
    def __init__(self, store: BaseVectorStore):
        self.store = store

    def retrieve(self, query: str, top_k: int) -> List[DocumentChunk]:
        return self.store.search(query, top_k)
