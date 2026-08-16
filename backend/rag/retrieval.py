
from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


# ============================================================
# CONFIGURATION
# ============================================================

CHROMA_HOST = "localhost"
CHROMA_PORT = 8000

COLLECTION_NAME = "personal_profile"

EMBEDDING_MODEL = "nomic-embed-text:latest"

TOP_K = 5


# ============================================================
# EMBEDDING MODEL
# ============================================================

def get_embedding_model():
    """
    Use the SAME embedding model that was used
    during document ingestion.
    """

    return OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url="http://localhost:11434",
    )


# ============================================================
# CHROMA VECTOR STORE
# ============================================================

def get_vector_store():
    """
    Connect to the ChromaDB collection.
    """

    embeddings = get_embedding_model()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        host=CHROMA_HOST,
        port=CHROMA_PORT,
    )

    return vector_store


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve_documents(
    vector_store,
    question,
    k=TOP_K,
):
    """
    Search ChromaDB for the most relevant chunks.
    """

    results = vector_store.similarity_search_with_score(
        question,
        k=k,
    )

    return results


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(
    question,
    results,
):
    """
    Print retrieved chunks and metadata.
    """

    print("\n")
    print("=" * 80)
    print("RETRIEVAL TEST")
    print("=" * 80)

    print("\nQUESTION:")
    print(question)

    print("\n" + "-" * 80)
    print("RETRIEVED DOCUMENTS")
    print("-" * 80)

    for index, (document, score) in enumerate(results):

        print(f"\n### RESULT {index + 1}")

        print("\nScore:")
        print(score)

        print("\nSource:")
        print(document.metadata.get("source"))

        print("\nDocument type:")
        print(document.metadata.get("document_type"))

        print("\nProject:")
        print(document.metadata.get("project"))

        print("\nChunk index:")
        print(document.metadata.get("chunk_index"))

        print("\nContent:")
        print(document.page_content)

        print("\n" + "-" * 80)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print("PERSONAL PROFILE RAG — RETRIEVAL TEST")
    print("=" * 80)

    # Connect to ChromaDB
    vector_store = get_vector_store()

    print("\nConnected to ChromaDB.")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Embedding model: {EMBEDDING_MODEL}")

    # --------------------------------------------------------
    # Interactive questions
    # --------------------------------------------------------

    while True:

        question = input(
            "\nAsk a question "
            "(type 'exit' to stop): "
        ).strip()

        if question.lower() == "exit":
            print("\nRetrieval test finished.")
            break

        if not question:
            continue

        results = retrieve_documents(
            vector_store=vector_store,
            question=question,
            k=TOP_K,
        )

        if not results:
            print("\nNo documents retrieved.")
            continue

        display_results(
            question=question,
            results=results,
        )


if __name__ == "__main__":
    main()
