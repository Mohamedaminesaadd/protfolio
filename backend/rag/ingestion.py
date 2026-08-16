from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

import chromadb

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from embeddings import get_embedding_model


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"

CHROMA_HOST = "localhost"
CHROMA_PORT = 8000

COLLECTION_NAME = "personal_profile"

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100


# ============================================================
# STEP 1 — FIND MARKDOWN FILES
# ============================================================

def find_markdown_files():
    """
    Find all .md files inside the knowledge directory.
    """

    files = list(KNOWLEDGE_DIR.rglob("*.md"))

    print("=" * 70)
    print("MARKDOWN FILES")
    print("=" * 70)

    for file in files:
        print(file.relative_to(PROJECT_ROOT))

    print(f"\nTotal files: {len(files)}")

    return files


# ============================================================
# STEP 2 — LOAD DOCUMENTS
# ============================================================

def load_documents(files):
    """
    Read every Markdown file and convert it into
    LangChain Document objects.
    """

    documents = []

    for file in files:

        text = file.read_text(
            encoding="utf-8"
        )

        relative_path = file.relative_to(KNOWLEDGE_DIR)

        # Determine document type
        if "projects" in file.parts:
            document_type = "project"
            project_name = file.stem
        elif file.stem == "skills":
            document_type = "skills"
            project_name = ""
        elif file.stem == "education":
            document_type = "education"
            project_name = ""
        elif file.stem == "profile":
            document_type = "profile"
            project_name = ""
        else:
            document_type = "other"
            project_name = ""

        metadata = {
            "source": str(relative_path),
            "file_name": file.name,
            "document_type": document_type,
            "project": project_name,
        }

        document = Document(
            page_content=text,
            metadata=metadata,
        )

        documents.append(document)

    print("\n" + "=" * 70)
    print("DOCUMENTS LOADED")
    print("=" * 70)

    print(f"Documents loaded: {len(documents)}")

    return documents


# ============================================================
# STEP 3 — CHUNK DOCUMENTS
# ============================================================

def split_documents(documents):
    """
    Split documents into smaller chunks.

    chunk_size:
        600 characters

    chunk_overlap:
        100 characters
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    print("\n" + "=" * 70)
    print("CHUNKING")
    print("=" * 70)

    print(f"Original documents : {len(documents)}")
    print(f"Generated chunks   : {len(chunks)}")
    print(f"Chunk size         : {CHUNK_SIZE}")
    print(f"Chunk overlap      : {CHUNK_OVERLAP}")

    return chunks


# ============================================================
# STEP 4 — ADD CHUNK METADATA
# ============================================================

def enrich_metadata(chunks):
    """
    Add a unique chunk ID and chunk index.
    """

    counters = {}

    for chunk in chunks:

        source = chunk.metadata["source"]

        if source not in counters:
            counters[source] = 0

        chunk_index = counters[source]

        chunk.metadata["chunk_index"] = chunk_index

        # Deterministic ID.
        # This makes the same document/chunk reproducible.
        chunk_id_string = (
            f"{source}:{chunk_index}"
        )

        chunk_id = str(
            uuid5(
                NAMESPACE_URL,
                chunk_id_string,
            )
        )

        chunk.metadata["chunk_id"] = chunk_id

        counters[source] += 1

    return chunks


# ============================================================
# STEP 5 — CONNECT TO CHROMADB
# ============================================================

def get_chroma():
    """
    Connect to ChromaDB running inside Docker.
    """

    client = chromadb.HttpClient(
        host=CHROMA_HOST,
        port=CHROMA_PORT,
    )

    # Test connection
    heartbeat = client.heartbeat()

    print("\n" + "=" * 70)
    print("CHROMADB")
    print("=" * 70)

    print("ChromaDB heartbeat:", heartbeat)

    embeddings = get_embedding_model()

    vector_store = Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

    return vector_store


# ============================================================
# STEP 6 — STORE DOCUMENTS
# ============================================================

def store_documents(vector_store, chunks):
    """
    Generate embeddings using nomic-embed-text
    and store them in ChromaDB.
    """

    print("\n" + "=" * 70)
    print("EMBEDDING + STORAGE")
    print("=" * 70)

    ids = [
        chunk.metadata["chunk_id"]
        for chunk in chunks
    ]

    vector_store.add_documents(
        documents=chunks,
        ids=ids,
    )

    print(f"Stored chunks: {len(chunks)}")
    print("Embedding model: nomic-embed-text:latest")


# ============================================================
# STEP 7 — VERIFY COLLECTION
# ============================================================

def verify_collection(vector_store):
    """
    Check how many chunks are stored.
    """

    collection = vector_store._collection

    count = collection.count()

    print("\n" + "=" * 70)
    print("COLLECTION VERIFICATION")
    print("=" * 70)

    print("Collection:", COLLECTION_NAME)
    print("Documents:", count)


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("PERSONAL PROFILE RAG — INGESTION PIPELINE")
    print("=" * 70)

    # 1. Find Markdown files
    files = find_markdown_files()

    if not files:
        print("No Markdown files found.")
        return

    # 2. Load documents
    documents = load_documents(files)

    # 3. Chunk documents
    chunks = split_documents(documents)

    # 4. Add metadata
    chunks = enrich_metadata(chunks)

    # Show examples
    print("\n" + "=" * 70)
    print("CHUNK EXAMPLES")
    print("=" * 70)

    for i, chunk in enumerate(chunks[:5]):

        print(f"\n--- Chunk {i} ---")

        print("Source:")
        print(chunk.metadata["source"])

        print("Chunk ID:")
        print(chunk.metadata["chunk_id"])

        print("Text:")
        print(chunk.page_content[:500])

    # 5. Connect to ChromaDB
    vector_store = get_chroma()

    # 6. Generate embeddings + store
    store_documents(
        vector_store,
        chunks,
    )

    # 7. Verify
    verify_collection(vector_store)

    print("\n" + "=" * 70)
    print("INGESTION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()