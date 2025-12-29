from typing import List

from langchain_huggingface import HuggingFaceEmbeddings

from config import settings
from core.embeddings.base import BaseEmbeddingProvider


class HuggingFaceEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self):
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
            )
        return self._model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.model.embed_query(text)
