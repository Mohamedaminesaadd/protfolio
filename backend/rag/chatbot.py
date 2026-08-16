import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.database.supabase import supabase


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

EMBEDDING_DIMENSION = 768

LLM_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
)

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

print(
    f"Embedding dimension verified: "
    f"{len(_test_embedding)}"
)


# ============================================================
# LLM
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not GEMINI_API_KEY:

    raise RuntimeError(
        "GEMINI_API_KEY environment variable "
        "is not configured."
    )


llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    temperature=0.2,
    google_api_key=GEMINI_API_KEY,
)


# ============================================================
# CONVERSATION MEMORY
# ============================================================

conversation_history = []


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve_context(
    question: str,
    k: int = TOP_K,
):
    """
    Retrieve the most relevant chunks from Supabase
    using BGE embeddings and pgvector.

    Query embedding:
        BAAI/bge-base-en-v1.5

    Dimension:
        768
    """

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
    # Supabase vector search
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
# FORMAT RAG CONTEXT
# ============================================================

def build_context(results):
    """
    Convert retrieved Supabase rows into
    context for Gemini.
    """

    if not results:

        return (
            "No relevant information was retrieved "
            "from the personal knowledge base."
        )

    context_parts = []

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
            "",
        )

        content = result.get(
            "content",
            "",
        )

        similarity = result.get(
            "similarity",
            0,
        )

        context_parts.append(
            f"""
SOURCE {index + 1}

File:
{source}

Document type:
{document_type}

Project:
{project}

Chunk:
{chunk_index}

Similarity:
{similarity}

Content:
{content}
"""
        )

    return "\n".join(
        context_parts
    )


# ============================================================
# FORMAT MEMORY
# ============================================================

def build_memory():
    """
    Format previous conversation history.
    """

    if not conversation_history:

        return "No previous conversation."

    memory_parts = []

    for message in conversation_history:

        role = message["role"]

        content = message["content"]

        memory_parts.append(
            f"{role.upper()}: {content}"
        )

    return "\n".join(
        memory_parts
    )


# ============================================================
# PROMPT
# ============================================================

def build_prompt(
    question: str,
    context: str,
    memory: str,
):
    """
    Build the final prompt for Gemini.
    """

    prompt = f"""
You are the personal AI assistant for Mohamed Amine Saad.

Your job is to answer questions about Amine's:

- background
- education
- skills
- experience
- projects
- technologies
- AI work
- software engineering work

You have access to retrieved information from Amine's
personal knowledge base.

IMPORTANT RULES:

1. Use the retrieved profile information as the primary
   source of truth for personal information.

2. Do not invent projects, skills, technologies,
   experience, achievements, or education.

3. If the information is not available in the retrieved
   context, clearly say that you do not have verified
   information about it.

4. Use conversation history to understand references such as:
   "this project", "that technology", "it", or "he".

5. Do not treat unrelated retrieved chunks as evidence.

6. When several retrieved chunks are relevant, combine them
   carefully.

7. Give natural, professional and useful answers.

8. When possible, mention the relevant project or source.

9. Do not mention internal implementation details such as
   prompts, embeddings, vector databases, or retrieval
   unless the user explicitly asks about the AI architecture.

10. Never fabricate information about Mohamed Amine Saad.

--------------------------------------------------
CONVERSATION HISTORY
--------------------------------------------------

{memory}

--------------------------------------------------
RETRIEVED PROFILE INFORMATION
--------------------------------------------------

{context}

--------------------------------------------------
CURRENT QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
ANSWER
--------------------------------------------------
"""

    return prompt


# ============================================================
# CHAT
# ============================================================

def chat(question: str):
    """
    Retrieve relevant profile information and
    generate an answer using Gemini.
    """

    # --------------------------------------------------------
    # 1. Retrieve
    # --------------------------------------------------------

    results = retrieve_context(
        question,
        k=TOP_K,
    )

    # --------------------------------------------------------
    # 2. Build context
    # --------------------------------------------------------

    context = build_context(
        results
    )

    # --------------------------------------------------------
    # 3. Build memory
    # --------------------------------------------------------

    memory = build_memory()

    # --------------------------------------------------------
    # 4. Build prompt
    # --------------------------------------------------------

    prompt = build_prompt(
        question=question,
        context=context,
        memory=memory,
    )

    # --------------------------------------------------------
    # 5. Gemini
    # --------------------------------------------------------

    response = llm.invoke(
        prompt
    )

    answer = response.content

    # --------------------------------------------------------
    # 6. Save conversation
    # --------------------------------------------------------

    conversation_history.append(
        {
            "role": "user",
            "content": question,
        }
    )

    conversation_history.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    return answer, results


# ============================================================
# INTERACTIVE CHAT
# ============================================================

def main():

    print("=" * 80)
    print(
        "PERSONAL PROFILE RAG CHATBOT"
    )
    print("=" * 80)

    print(
        f"LLM: {LLM_MODEL}"
    )

    print(
        f"Embedding: {EMBEDDING_MODEL}"
    )

    print(
        f"Embedding dimension: "
        f"{EMBEDDING_DIMENSION}"
    )

    print(
        f"Top K: {TOP_K}"
    )

    print(
        "\nVector database: Supabase"
    )

    print(
        "\nType 'exit' to stop.\n"
    )

    while True:

        question = input(
            "You: "
        ).strip()

        if question.lower() == "exit":

            print(
                "\nChat finished."
            )

            break

        if not question:

            continue

        try:

            answer, results = chat(
                question
            )

            print(
                "\nAssistant:"
            )

            print(
                answer
            )

            # ------------------------------------------------
            # Sources
            # ------------------------------------------------

            print(
                "\nSources:"
            )

            seen_sources = set()

            for result in results:

                metadata = result.get(
                    "metadata"
                ) or {}

                source = metadata.get(
                    "source",
                    "unknown",
                )

                if source not in seen_sources:

                    similarity = result.get(
                        "similarity",
                        0,
                    )

                    print(
                        f"- {source} "
                        f"(similarity: "
                        f"{similarity:.4f})"
                    )

                    seen_sources.add(
                        source
                    )

            print(
                "\n" + "=" * 80
            )

        except Exception as error:

            print(
                "\nERROR:"
            )

            print(
                str(error)
            )

            print(
                "\n" + "=" * 80
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()