from abc import ABC, abstractmethod
from typing import List

from core.models.document import Document


class BaseDocumentLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> List[Document]:
        pass
