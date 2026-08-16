import os

from dotenv import load_dotenv
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
)

from backend.database.supabase import supabase


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_MODEL = "gemini-embedding-2"

EMBEDDING_DIMENSION = 768

TOP_K = 5


# ============================================================
# EMBEDDING MODEL
# ============================================================

def get_embedding_model():
    """
    Create the Gemini Embedding 2 model.

    IMPORTANT:
    The query embedding MUST use exactly the same
    model and dimensionality used during ingestion.

    Model:
        gemini-embedding-2

    Dimension:
        768
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY environment variable "
            "is not set."
        )

    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=api_key,
        output_dimensionality=EMBEDDING_DIMENSION,
    )


# ============================================================
# LOAD MODEL ONCE
# ============================================================

print(
    f"Loading embedding model: "
    f"{EMBEDDING_MODEL}"
)

embeddings = get_embedding_model()

print(
    f"Embedding dimension: "
    f"{EMBEDDING_DIMENSION}"
)


# ============================================================
# VERIFY EMBEDDING MODEL
# ============================================================

def verify_embedding_model():
    """
    Verify that Gemini returns the expected
    vector dimension.
    """

    test_embedding = embeddings.embed_query(
        "What is HPIS?"
    )

    actual_dimension = len(
        test_embedding
    )

    if actual_dimension != EMBEDDING_DIMENSION:

        raise ValueError(
            f"Invalid embedding dimension. "
            f"Expected {EMBEDDING_DIMENSION}, "
            f"got {actual_dimension}"
        )

    print(
        "Embedding verification: OK"
    )


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve_documents(
    question: str,
    k: int = TOP_K,
):
    """
    Search Supabase pgvector using Gemini Embedding 2.
    """

    question = question.strip()

    if not question:
        return []

    # --------------------------------------------------------
    # Generate query embedding
    # --------------------------------------------------------

    query_embedding = embeddings.embed_query(
        question
    )

    # --------------------------------------------------------
    # Verify dimension
    # --------------------------------------------------------

    if len(query_embedding) != EMBEDDING_DIMENSION:

        raise ValueError(
            f"Invalid query embedding dimension. "
            f"Expected {EMBEDDING_DIMENSION}, "
            f"got {len(query_embedding)}"
        )

    # --------------------------------------------------------
    # Search Supabase
    # --------------------------------------------------------

    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": k,
        },
    ).execute()

    return response.data or []


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(
    question,
    results,
):
    """
    Display retrieved chunks.
    """

    print("\n")
    print("=" * 80)
    print("SUPABASE RAG RETRIEVAL TEST")
    print("=" * 80)

    print("\nQUESTION:")
    print(question)

    print(
        f"\nEmbedding model: "
        f"{EMBEDDING_MODEL}"
    )

    print(
        f"Embedding dimension: "
        f"{EMBEDDING_DIMENSION}"
    )

    print("\n" + "-" * 80)
    print("RETRIEVED DOCUMENTS")
    print("-" * 80)

    if not results:

        print("\nNo documents retrieved.")

        return

    for index, result in enumerate(results):

        print(
            f"\n### RESULT {index + 1}"
        )

        print("\nSimilarity:")

        print(
            result.get(
                "similarity",
                0,
            )
        )

        metadata = (
            result.get("metadata")
            or {}
        )

        print("\nSource:")

        print(
            metadata.get(
                "source",
                "unknown",
            )
        )

        print("\nDocument type:")

        print(
            metadata.get(
                "document_type",
                "unknown",
            )
        )

        print("\nProject:")

        print(
            metadata.get(
                "project",
                "",
            )
        )

        print("\nChunk index:")

        print(
            metadata.get(
                "chunk_index",
                "unknown",
            )
        )

        print("\nContent:")

        print(
            result.get(
                "content",
                "",
            )
        )

        print(
            "\n" + "-" * 80
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)

    print(
        "PERSONAL PROFILE RAG"
    )

    print(
        "SUPABASE RETRIEVAL TEST"
    )

    print("=" * 80)

    print(
        f"\nEmbedding model: "
        f"{EMBEDDING_MODEL}"
    )

    print(
        f"Embedding dimension: "
        f"{EMBEDDING_DIMENSION}"
    )

    print(
        f"Top K: {TOP_K}"
    )

    # --------------------------------------------------------
    # Verify model once
    # --------------------------------------------------------

    print(
        "\nVerifying embedding model..."
    )

    try:

        verify_embedding_model()

    except Exception as error:

        print(
            "\nEmbedding verification failed:"
        )

        print(error)

        return

    # --------------------------------------------------------
    # Interactive retrieval
    # --------------------------------------------------------

    while True:

        question = input(
            "\nAsk a question "
            "(type 'exit' to stop): "
        ).strip()

        if question.lower() == "exit":

            print(
                "\nRetrieval test finished."
            )

            break

        if not question:
            continue

        try:

            results = retrieve_documents(
                question=question,
                k=TOP_K,
            )

            display_results(
                question=question,
                results=results,
            )

        except Exception as error:

            print(
                "\nRetrieval error:"
            )

            print(error)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()