from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.database.supabase import supabase


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_MODEL = "gemini-embedding-2"

EMBEDDING_DIMENSION = 768

TOP_K = 5


# ============================================================
# EMBEDDINGS
# ============================================================

embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    output_dimensionality=EMBEDDING_DIMENSION,
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

    The tool uses Gemini Embedding 2 to search
    Supabase pgvector.
    """

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    question = question.strip()

    if not question:
        return "No question was provided."

    # --------------------------------------------------------
    # Generate query embedding
    # --------------------------------------------------------

    try:
        query_embedding = embeddings.embed_query(
            question
        )

    except Exception as error:

        return (
            "Unable to generate the search embedding. "
            f"Embedding error: {error}"
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

    try:

        response = supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_count": TOP_K,
            },
        ).execute()

    except Exception as error:

        return (
            "Unable to search the personal knowledge base. "
            f"Database error: {error}"
        )

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

    print(
        "\nQuestion:"
    )

    print(question)

    print(
        "\nGenerating Gemini embedding..."
    )

    try:

        test_embedding = embeddings.embed_query(
            question
        )

        print(
            f"Embedding dimension: "
            f"{len(test_embedding)}"
        )

        if len(test_embedding) != EMBEDDING_DIMENSION:

            raise ValueError(
                f"Expected {EMBEDDING_DIMENSION} "
                f"dimensions, got "
                f"{len(test_embedding)}"
            )

        print(
            "Embedding dimension: OK"
        )

        print(
            "\nSearching Supabase..."
        )

        result = search_profile.invoke(
            {
                "question": question
            }
        )

        print(
            "\nRetrieved context:"
        )

        print(result)

    except Exception as error:

        print(
            "\nRAG TOOL ERROR:"
        )

        print(error)