from typing import List, Optional
from pydantic import BaseModel


class PaperSection(BaseModel):
    section_id: str
    title: str
    content: str


class CitationRelationship(BaseModel):
    citing_paper_id: str
    cited_paper_id: str
    context: Optional[str] = None


class ResearchPaper(BaseModel):
    paper_id: str
    title: str
    authors: List[str]
    abstract: str
    full_text: Optional[str] = None
    year: int
    venue: Optional[str] = None
    keywords: List[str] = []
    sections: List[PaperSection] = []
    references: List[str] = []          # paper_ids this paper cites
    citations: List[str] = []           # paper_ids that cite this paper
