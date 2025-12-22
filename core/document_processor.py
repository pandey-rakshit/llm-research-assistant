from typing import List, Dict, Optional
from pathlib import Path
from config import settings
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    
    def __init__(self, chunk_size:int = None, chunk_overlap:int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function = len,
            separators = ["\n\n", "\n", " ", ""]
        )

        self._metadata = dict()
    
    def load_document(self, file_path:str = None) -> List[Document]:
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension == 'pdf':
            loader = PyPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file {extension} extention. Use .pdf file")

        return loader.load()

    def load_metadata(self, documents: List[Document] = None) -> Dict:
        self._metadata = documents[0].metadata or dict()
        return self._metadata


    def split_document(self, documents: List[Document] = None) -> List[Document]:
        return self.text_splitter.split_documents(documents)

    def process(self, file_path: str = None):
        documents = self.load_document(file_path)
        metadata = self.load_metadata(documents)
        chunks = self.split_document(documents)
        return chunks, metadata
