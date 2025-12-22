
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"  # Free HuggingFace model

settings = Settings()