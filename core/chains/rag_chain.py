from core.llm.base import BaseLLMProvider
from core.retriever.retriever import RetrieverService


class RAGChain:
    def __init__(
        self,
        retriever: RetrieverService,
        llm: BaseLLMProvider,
    ):
        self.retriever = retriever
        self.llm = llm

    def run(self, query: str):
        chunks = self.retriever.retrieve(query, top_k=5)

        context = "\n\n".join(c.content for c in chunks)

        sources = []
        for c in chunks:
            filename = c.metadata.get("title", "document")
            section = c.metadata.get("section", "Unknown section")
            chunk_index = c.metadata.get("chunk_index", "?")

            sources.append(f"📄 {filename} — {section} — chunk {chunk_index}")

        prompt = f"""
            Answer using only the context below.

            Context:
            {context}

            Question:
            {query}
            """

        answer = self.llm.generate(prompt)
        return answer, list(dict.fromkeys(sources))
