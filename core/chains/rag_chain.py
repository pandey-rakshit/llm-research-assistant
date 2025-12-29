import json
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
        # -----------------------------------------
        # 1. Intent + optional response in ONE call
        # -----------------------------------------
        intent_prompt = f"""
        You are an assistant for a document-based QA system.

        Classify the user input and respond in JSON.

        Rules:
        - If it is a greeting, return a friendly response.
        - If it is unrelated to the document, say you don't have information.
        - If it is a document question, set response to null.

        Return ONLY valid JSON.

        Format:
        {{
        "intent": "greeting | document_question | out_of_context",
        "response": string | null
        }}

        User input:
        "{query}"
        """
        result = json.loads(self.llm.generate(intent_prompt))

        intent = result["intent"]
        response = result["response"]

        # -----------------------------------------
        # 2. Greeting or out-of-context → DONE
        # -----------------------------------------
        if intent in {"greeting", "out_of_context"}:
            return response, []

        # -----------------------------------------
        # 3. Document question → RAG
        # -----------------------------------------
        chunks = self.retriever.retrieve(query, top_k=5)

        if not chunks:
            return (
                "I don’t have information about that in the document.",
                [],
            )

        context = "\n\n".join(c.content for c in chunks)

        sources = []
        for c in chunks:
            filename = c.metadata.get("title", "document")
            section = c.metadata.get("section", "Full Document")
            chunk_index = c.metadata.get("chunk_index", "?")

            sources.append(
                f"📄 {filename} — {section} — chunk {chunk_index}"
            )

        answer_prompt = f"""
        Answer the question using ONLY the context below.
        If the answer is not present, say you do not know.

        Context:
        {context}

        Question:
        {query}
        """
        answer = self.llm.generate(answer_prompt)

        return answer, list(dict.fromkeys(sources))
