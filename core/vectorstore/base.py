from abc import ABC, abstractmethod
from typing import List

from core.models.document import DocumentChunk


class BaseVectorStore(ABC):
    @abstractmethod
    def add(self, chunks: List[DocumentChunk]) -> None:
        pass

    @abstractmethod
    def search(self, query: str, top_k: int) -> List[DocumentChunk]:
        pass
