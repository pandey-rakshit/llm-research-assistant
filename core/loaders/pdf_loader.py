import uuid
from typing import List

from langchain_community.document_loaders import PyPDFLoader

from core.loaders.base import BaseDocumentLoader
from core.models.document import Document


class PDFDocumentLoader(BaseDocumentLoader):
    def load(self, path: str) -> List[Document]:
        pages = PyPDFLoader(path).load()
        text = "\n".join(p.page_content for p in pages)

        return [
            Document(
                document_id=str(uuid.uuid4()),
                source_type="pdf",
                source_uri=path,
                content=text,
                metadata=pages[0].metadata,
            )
        ]
