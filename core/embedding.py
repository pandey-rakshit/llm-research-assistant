from typing import List
from config import settings
from langchain_huggingface import HuggingFaceEmbeddings
class EmbeddingManager:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self._embedding = HuggingFaceEmbeddings(
            model_name = self.model_name,
            model_kwargs = {"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}  # Normalize for cosine similarity
        )

    @property
    def embeddings(self) -> HuggingFaceEmbeddings:
        return self._embedding
    
    def embed_text(self, text:str) -> List[float]:
        return self._embedding.embed_query(text)

    def embed_document(self, document: List[str]) -> List[List[float]]:
        return self._embedding.aembed_documents(document)
    
    def get_embedding_dimension(self) -> int:
        sample_embedding = self.embed_text("sample")
        return len(sample_embedding)
