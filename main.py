from core import DocumentProcessor, EmbeddingManager, VectorStoreManager
import pprint

def main():
    print("Hello from llm-research-assistant!")

    print("="*70)
    print("Part I: Paper Ingestion & Representation (Python + LangChain)")
    print("="*70)

    processor = DocumentProcessor()
    chunks, metadata, sections = processor.process("./docs/generative_refocusing.pdf")
    print(f"✅ Document processed into {len(chunks)} chunks")
    
    print("\n" + "="*70)
    print(f"Research Paper Metadata: \n")
    
    pprint.pprint(metadata, indent=4)
    
    print("\n" + "="*70)
    print(f"Research Paper Sections: \n")
    
    pprint.pprint(sections, indent=4)
    
    print("\n" + "="*70)

    print("Part II: Knowledge Indexing & Semantic Search (FAISS + LangChain)")
    print("="*70)

    embedder = EmbeddingManager()
    
    print("✅ Embedding model loaded")
    
    print(f"   Model: {embedder.model_name}")
    print(f"   Dimension: {embedder.get_embedding_dimension()}")
    
    print("="*70)
    
    print("\n📊 Building vector store...")
    
    vs_manager = VectorStoreManager(embedder)
    vs_manager.create_from_documents(chunks)
    
    print(f"✅ Vector store created with {len(chunks)} documents")
    print("="*70)
    
    # Test semantic search
    print("\n🔍 Testing semantic search...")
    
    test_queries = [
        "What is generative refocusing",
        "what is Artifact-robust dual conditioning"
    ]
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        results = vs_manager.search(query, k=2)
        
        for i, doc in enumerate(results, 1):
            print(f"   {i}. {doc.page_content}...")
    
    print("="*70)
    # Save vector store
    print("\n💾 Saving vector store...")
    
    vs_manager.save()
    
    print(f"✅ Vector store saved to {vs_manager.index_path}/")
    print("="*70)
    
    # Load and verify
    print("\n📂 Loading saved vector store...")
    
    vs_loader = VectorStoreManager(embedder)
    vs_loader.load()
    
    print("✅ Vector store loaded successfully")

    print("="*70)

    
    # Verify it works
    test_result = vs_loader.search("generative refocusing", k=1)
    print(f"✅ Verification search returned: {test_result[0].page_content[:200]}...")


if __name__ == "__main__":
    main()
