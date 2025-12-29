from core.chains.rag_chain import RAGChain
from core.embeddings.huggingface import HuggingFaceEmbeddingProvider
from core.llm.groq import GroqLLMProvider
from core.loaders.pdf_loader import PDFDocumentLoader
from core.pipeline.document_pipeline import DocumentIngestionPipeline
from core.processors.chunker import DocumentChunker
from core.processors.section_extractor import SectionExtractor
from core.retriever.retriever import RetrieverService
from core.vectorstore.faiss_store import FAISSVectorStore
from orchestrator import KnowledgeBaseOrchestrator


def build_rag_system():
    loader = PDFDocumentLoader()
    extractor = SectionExtractor()
    chunker = DocumentChunker()

    embedding = HuggingFaceEmbeddingProvider()
    store = FAISSVectorStore(embedding)

    pipeline = DocumentIngestionPipeline(
        loader=loader,
        extractor=extractor,
        chunker=chunker,
    )

    orchestrator = KnowledgeBaseOrchestrator(pipeline, store)

    retriever = RetrieverService(store)
    llm = GroqLLMProvider()
    rag_chain = RAGChain(retriever, llm)

    return orchestrator, rag_chain
