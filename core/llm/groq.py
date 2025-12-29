from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from config import settings
from core.llm.base import BaseLLMProvider


class GroqLLMProvider(BaseLLMProvider):
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
        )

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
