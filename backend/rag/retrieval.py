from langchain_huggingface import HuggingFaceEmbeddings

from backend.database.supabase import supabase


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

EMBEDDING_DIMENSION = 768

TOP_K = 5


# ============================================================
# EMBEDDING MODEL
# ============================================================

def get_embedding_model():
    """
    Use the SAME embedding model that was used
    during document ingestion.

    Model:
        BAAI/bge-base-en-v1.5

    Dimension:
        768
    """

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve_documents(
    question,
    k=TOP_K,
):
    """
    Search Supabase pgvector for the most
    relevant chunks.
    """

    embeddings = get_embedding_model()

    # --------------------------------------------------------
    # Generate embedding for the question
    # --------------------------------------------------------

    query_embedding = embeddings.embed_query(
        question
    )

    # --------------------------------------------------------
    # Verify embedding dimension
    # --------------------------------------------------------

    if len(query_embedding) != EMBEDDING_DIMENSION:

        raise ValueError(
            f"Invalid embedding dimension: "
            f"expected {EMBEDDING_DIMENSION}, "
            f"got {len(query_embedding)}"
        )

    # --------------------------------------------------------
    # Call Supabase PostgreSQL function
    # --------------------------------------------------------

    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": k,
        },
    ).execute()

    return response.data


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
    print("SUPABASE RAG RETRIEVAL TEST")
    print("=" * 80)

    print("\nQUESTION:")
    print(question)

    print("\n" + "-" * 80)
    print("RETRIEVED DOCUMENTS")
    print("-" * 80)

    for index, result in enumerate(results):

        print(
            f"\n### RESULT {index + 1}"
        )

        print("\nSimilarity:")
        print(
            result.get("similarity")
        )

        metadata = result.get(
            "metadata"
        ) or {}

        print("\nSource:")
        print(
            metadata.get("source")
        )

        print("\nDocument type:")
        print(
            metadata.get("document_type")
        )

        print("\nProject:")
        print(
            metadata.get("project")
        )

        print("\nChunk index:")
        print(
            metadata.get("chunk_index")
        )

        print("\nContent:")
        print(
            result.get("content")
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
        "PERSONAL PROFILE RAG — "
        "SUPABASE RETRIEVAL TEST"
    )

    print("=" * 80)

    print("\nConnected to Supabase.")

    print(
        f"Embedding model: "
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
    # Load embedding model ONCE
    # --------------------------------------------------------

    print(
        "\nLoading embedding model..."
    )

    embeddings = get_embedding_model()

    print(
        "Embedding model loaded."
    )

    # --------------------------------------------------------
    # Interactive questions
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

            # ------------------------------------------------
            # Generate query embedding
            # ------------------------------------------------

            query_embedding = (
                embeddings.embed_query(
                    question
                )
            )

            # ------------------------------------------------
            # Verify dimension
            # ------------------------------------------------

            if len(query_embedding) != EMBEDDING_DIMENSION:

                raise ValueError(
                    f"Expected "
                    f"{EMBEDDING_DIMENSION} dimensions, "
                    f"got "
                    f"{len(query_embedding)}"
                )

            # ------------------------------------------------
            # Search Supabase
            # ------------------------------------------------

            response = supabase.rpc(
                "match_documents",
                {
                    "query_embedding": query_embedding,
                    "match_count": TOP_K,
                },
            ).execute()

            results = response.data

            if not results:

                print(
                    "\nNo documents retrieved."
                )

                continue

            # ------------------------------------------------
            # Display
            # ------------------------------------------------

            display_results(
                question=question,
                results=results,
            )

        except Exception as e:

            print(
                "\nRetrieval error:"
            )

            print(e)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()