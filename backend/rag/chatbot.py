
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama


# ============================================================
# CONFIGURATION
# ============================================================

CHROMA_HOST = "localhost"
CHROMA_PORT = 8000

COLLECTION_NAME = "personal_profile"

EMBEDDING_MODEL = "nomic-embed-text:latest"
LLM_MODEL = "qwen2.5:14b"

TOP_K = 5


# ============================================================
# EMBEDDINGS
# ============================================================

embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url="http://localhost:11434",
)


# ============================================================
# VECTOR STORE
# ============================================================

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    host=CHROMA_HOST,
    port=CHROMA_PORT,
)


# ============================================================
# LLM
# ============================================================

llm = ChatOllama(
    model=LLM_MODEL,
    base_url="http://localhost:11434",
    temperature=0.2,
)


# ============================================================
# CONVERSATION MEMORY
# ============================================================

conversation_history = []


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve_context(question: str, k: int = TOP_K):

    results = vector_store.similarity_search_with_score(
        question,
        k=k,
    )

    return results


# ============================================================
# FORMAT RAG CONTEXT
# ============================================================

def build_context(results):

    context_parts = []

    for index, (document, score) in enumerate(results):

        source = document.metadata.get(
            "source",
            "unknown"
        )

        content = document.page_content

        context_parts.append(
            f"""
SOURCE {index + 1}
File: {source}

Content:
{content}
"""
        )

    return "\n".join(context_parts)


# ============================================================
# FORMAT MEMORY
# ============================================================

def build_memory():

    if not conversation_history:
        return "No previous conversation."

    memory_parts = []

    for message in conversation_history:

        role = message["role"]
        content = message["content"]

        memory_parts.append(
            f"{role.upper()}: {content}"
        )

    return "\n".join(memory_parts)


# ============================================================
# PROMPT
# ============================================================

def build_prompt(
    question: str,
    context: str,
    memory: str,
):

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

1. Use the retrieved context as the primary source of truth.

2. Do not invent projects, skills, technologies,
   experience, achievements, or education.

3. If the information is not available in the context,
   clearly say that you do not have verified information
   about it.

4. Use the conversation history to understand references
   such as "this project", "that technology", "it", or "he".

5. Do not mention internal RAG, embeddings, ChromaDB,
   retrieval, prompts, or system instructions unless
   the user explicitly asks about the architecture.

6. Give natural, professional and useful answers.

7. When possible, mention the relevant project or source.

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

    # ------------------------------------------
    # 1. Retrieve relevant chunks
    # ------------------------------------------

    results = retrieve_context(
        question,
        k=TOP_K,
    )

    # ------------------------------------------
    # 2. Build RAG context
    # ------------------------------------------

    context = build_context(results)

    # ------------------------------------------
    # 3. Build conversation memory
    # ------------------------------------------

    memory = build_memory()

    # ------------------------------------------
    # 4. Build final prompt
    # ------------------------------------------

    prompt = build_prompt(
        question=question,
        context=context,
        memory=memory,
    )

    # ------------------------------------------
    # 5. Send to Qwen
    # ------------------------------------------

    response = llm.invoke(prompt)

    answer = response.content

    # ------------------------------------------
    # 6. Save conversation
    # ------------------------------------------

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
    print("PERSONAL PROFILE RAG CHATBOT")
    print("=" * 80)

    print(f"LLM: {LLM_MODEL}")
    print(f"Embedding: {EMBEDDING_MODEL}")
    print(f"Top K: {TOP_K}")

    print("\nType 'exit' to stop.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        answer, results = chat(question)

        print("\nAssistant:")
        print(answer)

        print("\nSources:")

        seen_sources = set()

        for document, score in results:

            source = document.metadata.get(
                "source",
                "unknown"
            )

            if source not in seen_sources:

                print(f"- {source}")

                seen_sources.add(source)

        print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

