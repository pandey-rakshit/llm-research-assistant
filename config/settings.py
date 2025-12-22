
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    
    # Document Processing Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Embedding Configuration  
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"  # Free HuggingFace model
    
    # Vector Store Configuration
    FAISS_INDEX_PATH: str = "data/faiss_index"

    # Retrieval Configuration
    TOP_K_RESULTS: int = 3

settings = Settings()