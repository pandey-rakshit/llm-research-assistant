from typing import List, Optional
from config import settings
import os
from core import EmbeddingManager
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class VectorStoreManager:
    def __init__(self, embedding_manager: EmbeddingManager = None):
        self.embedding_manager = embedding_manager or EmbeddingManager()
        self._vector_store: Optional[FAISS] = None
        self.index_path = settings.FAISS_INDEX_PATH

    @property
    def vector_store(self) -> Optional[FAISS]:
        return self._vector_store

    @property
    def is_initialized(self) -> bool:
        return self._vector_store is not None

    def create_from_documents(self, documents: List[Document]) -> FAISS:
        self._vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embedding_manager.embeddings
        )

        return self._vector_store

    def add_documents(self, documents: List[Document]) -> None:
        if not self.is_initialized:
            self.create_from_documents(documents)
        else:
            self._vector_store.add_documents(documents)

    def search(self, query: str, k: int = None) -> List[Document]:
        if not self.is_initialized:
            raise ValueError(f"Vector store is not Initialized. Add documents first.")
        
        k = k or settings.TOP_K_RESULTS
        return self._vector_store.similarity_search(query, k=k)
    
    def search_with_scores(self, query: str, k:int = None) -> List[tuple]:
        if not self.is_initialized:
            raise ValueError(f"Vector store is not Initialized. Add documents first.")
        
        k = k or settings.TOP_K_RESULTS
        return self._vector_store.similarity_search_with_score(query, k=k)

    def save(self, path: str = None) -> None:
        if not self.is_initialized:
            raise ValueError("Vector store is not initialized. Nothing to save.")
        
        save_path = path or self.index_path
        os.makedirs(save_path, exist_ok=True)
        self._vector_store.save_local(save_path)
    
    def load(self, path: str = None) -> FAISS:
        load_path = path or self.index_path
        
        if not os.path.exists(load_path):
            raise FileNotFoundError(f"No saved index found at {load_path}")
        
        self._vector_store = FAISS.load_local(
            load_path,
            self.embedding_manager.embeddings,
            allow_dangerous_deserialization=True  # Required for loading
        )
        return self._vector_store

    def get_retriever(self, k: int = None):
        if not self.is_initialized:
            raise ValueError("Vector store is not initialized.")
        
        k = k or settings.TOP_K_RESULTS
        return self._vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
    
    def clear(self) -> None:
        self._vector_store = None

