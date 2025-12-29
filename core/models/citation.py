from dataclasses import dataclass


@dataclass(frozen=True)
class Citation:
    source_paper_id: str
    cited_title: str
