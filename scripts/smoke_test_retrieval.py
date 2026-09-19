import sys
from pathlib import Path

# Add project root so `core` imports work when this file
# is executed directly from the scripts directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from core.rag.retriever import LocalRetriever


def main():
    knowledge_base = PROJECT_ROOT / "data" / "knowledge_base" / "risk_restructuring"
    retriever = LocalRetriever(str(knowledge_base))

    queries = [
        "What information is needed before comparing restructuring options?",
        "When should a risk case be escalated?",
        "Can the AI approve a restructuring?",
    ]

    for query in queries:
        print("\n" + "=" * 70)
        print("QUERY:", query)

        results = retriever.search(query, top_k=3)

        for result in results:
            print(f"\nSource: {result.document_name}")
            print(f"Chunk: {result.chunk_id}")
            print(f"Score: {result.relevance_score:.3f}")
            print(f"Excerpt: {result.excerpt[:350]}")


if __name__ == "__main__":
    main()
