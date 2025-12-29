from core.llm.base import BaseLLMProvider
from core.models.document import Document


class SummarizationChain:
    """
    Paper-level summarization.
    Uses full document content ONLY.
    No section-based chunking.
    """

    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    def summarize(self, document: Document) -> str:
        prompt = f"""
        You are an academic research assistant.

        Provide a concise, high-level summary of the paper covering:
        - Problem motivation
        - Core idea / method
        - Key results
        - Broader implications

        Paper:
        {document.content}

        Summary:
        """.strip()

        return self.llm.generate(prompt)
