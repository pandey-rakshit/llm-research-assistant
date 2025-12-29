from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class Document:
    document_id: str
    source_type: str
    source_uri: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DocumentSection:
    document_id: str
    section_name: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DocumentChunk:
    document_id: str
    chunk_id: str
    content: str
    metadata: Dict[str, Any]
