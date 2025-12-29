from typing import Dict, List

from core.models.document import Document, DocumentSection

SECTION_TITLES = {
    "abstract",
    "introduction",
    "methods",
    "methodology",
    "experiments",
    "results",
    "discussion",
    "conclusion",
    "references",
}


class PDFHeuristicSectionExtractor:
    def _normalize(self, line: str) -> str:
        line = line.strip().lower()
        line = line.lstrip("0123456789. ")
        return line.strip()

    def extract(self, document: Document) -> List[DocumentSection]:
        sections: Dict[str, List[str]] = {}
        current = "full document"

        for line in document.content.splitlines():
            line = line.strip()
            if not line:
                continue

            normalized = self._normalize(line)

            if normalized in SECTION_TITLES:
                current = normalized
                sections.setdefault(current, [])
                continue

            sections.setdefault(current, []).append(line)

        real_sections = [k for k in sections if k != "full document"]
        if len(real_sections) < 2:
            return [
                DocumentSection(
                    document_id=document.document_id,
                    section_name="Full Document",
                    content=document.content,
                    metadata=document.metadata,
                )
            ]

        return [
            DocumentSection(
                document_id=document.document_id,
                section_name=section.title(),
                content="\n".join(content),
                metadata=document.metadata,
            )
            for section, content in sections.items()
        ]
