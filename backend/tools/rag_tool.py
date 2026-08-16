
from langchain_core.tools import tool
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
# EMBEDDINGS
# ============================================================

embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url="http://localhost:11434",
)


# ============================================================
# CHROMA
# ============================================================

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    host=CHROMA_HOST,
    port=CHROMA_PORT,
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
    - LLMs
    - LangChain
    - LangGraph
    - PyTorch
    - backend
    - Docker
    - project architecture
    - datasets
    """

    # --------------------------------------------------------
    # Retrieve documents
    # --------------------------------------------------------

    results = vector_store.similarity_search_with_score(
        question,
        k=TOP_K,
    )

    if not results:
        return (
            "No relevant information was found "
            "in the personal knowledge base."
        )

    # --------------------------------------------------------
    # Format retrieved context
    # --------------------------------------------------------

    context = []

    for index, (document, score) in enumerate(results):

        metadata = document.metadata

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

        content = document.page_content

        context.append(
            f"""
--- RESULT {index + 1} ---

Source: {source}

Document type: {document_type}

Project: {project}

Chunk: {chunk_index}

Content:
{content}

Retrieval score:
{score}
"""
        )

    return "\n".join(context)


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    question = "What is HPIS?"

    result = search_profile.invoke(
        {
            "question": question
        }
    )

    print("=" * 80)
    print("RAG TOOL TEST")
    print("=" * 80)

    print("\nQuestion:")
    print(question)

    print("\nRetrieved context:")
    print(result)
