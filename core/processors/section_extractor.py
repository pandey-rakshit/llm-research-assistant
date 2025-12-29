from core.models.document import Document, DocumentSection
from core.processors.pdf_section_extractor import PDFHeuristicSectionExtractor


class SectionExtractor:
    def __init__(self):
        self.pdf_extractor = PDFHeuristicSectionExtractor()

    def extract(self, document: Document) -> list[DocumentSection]:
        if document.source_type == "pdf":
            return self.pdf_extractor.extract(document)

        return [
            DocumentSection(
                document_id=document.document_id,
                section_name="Full Document",
                content=document.content,
                metadata=document.metadata,
            )
        ]
