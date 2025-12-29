from typing import Dict, List

from core.models.citation import Citation


class CitationGraph:
    def __init__(self):
        self.graph: Dict[str, List[str]] = {}

    def add(self, citation: Citation):
        self.graph.setdefault(citation.source_paper_id, []).append(citation.cited_title)
