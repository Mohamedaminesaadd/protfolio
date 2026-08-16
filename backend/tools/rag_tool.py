from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings

from backend.database.supabase import supabase


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

EMBEDDING_DIMENSION = 768

TOP_K = 5


# ============================================================
# EMBEDDINGS
# ============================================================

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={
        "device": "cpu",
    },
    encode_kwargs={
        "normalize_embeddings": True,
    },
)


# ============================================================
# VERIFY EMBEDDING DIMENSION
# ============================================================

_test_embedding = embeddings.embed_query(
    "What is HPIS?"
)

if len(_test_embedding) != EMBEDDING_DIMENSION:

    raise ValueError(
        f"Invalid embedding dimension. "
        f"Expected {EMBEDDING_DIMENSION}, "
        f"got {len(_test_embedding)}"
    )


# ============================================================
# RAG TOOL
# ============================================================

@tool
def search_profile(question: str) -> str:
    """
    Search Mohamed Amine Saad's personal knowledge base.

    Use this tool for questions about:

    - profile
    - education
    - skills
    - experience
    - projects
    - technologies
    - AI
    - machine learning
    - deep learning
    - computer vision
    - NLP
    - LLMs
    - LangChain
    - LangGraph
    - PyTorch
    - backend
    - Docker
    - project architecture
    - datasets

    The tool retrieves relevant information from the
    personal knowledge base using BGE embeddings and
    Supabase pgvector.
    """

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    question = question.strip()

    if not question:

        return (
            "No question was provided."
        )

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
    # Search Supabase / pgvector
    # --------------------------------------------------------

    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": TOP_K,
        },
    ).execute()

    results = response.data

    # --------------------------------------------------------
    # No results
    # --------------------------------------------------------

    if not results:

        return (
            "No relevant information was found "
            "in Mohamed Amine Saad's personal "
            "knowledge base."
        )

    # --------------------------------------------------------
    # Format retrieved context
    # --------------------------------------------------------

    context = []

    for index, result in enumerate(results):

        metadata = result.get(
            "metadata"
        ) or {}

        source = metadata.get(
            "source",
            "unknown",
        )

        document_type = metadata.get(
            "document_type",
            "unknown",
        )

        project = metadata.get(
            "project",
            "",
        )

        chunk_index = metadata.get(
            "chunk_index",
            "unknown",
        )

        content = result.get(
            "content",
            "",
        )

        similarity = result.get(
            "similarity",
            0,
        )

        context.append(
            f"""
--- RESULT {index + 1} ---

Source: {source}

Document type: {document_type}

Project: {project}

Chunk: {chunk_index}

Similarity: {similarity}

Content:
{content}
"""
        )

    return "\n".join(context)


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    question = "What is HPIS?"

    print("=" * 80)
    print("RAG TOOL TEST")
    print("=" * 80)

    print(
        f"\nEmbedding model:"
        f" {EMBEDDING_MODEL}"
    )

    print(
        f"Embedding dimension:"
        f" {EMBEDDING_DIMENSION}"
    )

    print(
        f"Top K: {TOP_K}"
    )

    print(
        "\nQuestion:"
    )

    print(
        question
    )

    print(
        "\nSearching Supabase..."
    )

    try:

        result = search_profile.invoke(
            {
                "question": question
            }
        )

        print(
            "\nRetrieved context:"
        )

        print(
            result
        )

    except Exception as error:

        print(
            "\nRAG TOOL ERROR:"
        )

        print(
            error
        )