import os

from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.rag.embeddings import get_embedding_model
from backend.database.supabase import supabase


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 80

TABLE_NAME = "documents"

# Gemini Embedding 2
EMBEDDING_MODEL_NAME = "gemini-embedding-2"

# Recommended reduced dimension for Gemini Embedding 2
EMBEDDING_DIMENSION = 768


# ============================================================
# STEP 1 — FIND MARKDOWN FILES
# ============================================================

def find_markdown_files():
    """Find all Markdown files inside the knowledge directory."""

    files = sorted(
        KNOWLEDGE_DIR.rglob("*.md")
    )

    print("=" * 70)
    print("MARKDOWN FILES")
    print("=" * 70)

    for file in files:

        print(
            f"  {file.relative_to(PROJECT_ROOT)}"
        )

    print(
        f"\nTotal files: {len(files)}"
    )

    return files


# ============================================================
# STEP 2 — DETERMINE DOCUMENT TYPE
# ============================================================

def get_document_metadata(file: Path):
    """Build metadata for a knowledge file."""

    relative_path = file.relative_to(
        KNOWLEDGE_DIR
    )

    parts = file.parts

    if "projects" in parts:

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

    elif file.stem in {
        "experience",
        "expercience",
    }:

        document_type = "experience"
        project_name = ""

    else:

        document_type = "other"
        project_name = ""

    return {
        "source": str(relative_path),
        "file_name": file.name,
        "document_type": document_type,
        "project": project_name,
    }


# ============================================================
# STEP 3 — LOAD DOCUMENTS
# ============================================================

def load_documents(files):
    """Load Markdown files into LangChain Documents."""

    documents = []

    for file in files:

        text = file.read_text(
            encoding="utf-8"
        ).strip()

        if not text:

            print(
                f"Skipping empty file: {file}"
            )

            continue

        metadata = get_document_metadata(
            file
        )

        document = Document(
            page_content=text,
            metadata=metadata,
        )

        documents.append(
            document
        )

    print(
        "\n" + "=" * 70
    )

    print(
        "DOCUMENTS LOADED"
    )

    print(
        "=" * 70
    )

    print(
        f"Documents loaded: "
        f"{len(documents)}"
    )

    return documents


# ============================================================
# STEP 4 — CHUNK DOCUMENTS
# ============================================================

def split_documents(documents):
    """
    Split documents while preserving
    Markdown structure where possible.
    """

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=CHUNK_SIZE,

        chunk_overlap=CHUNK_OVERLAP,

        separators=[
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "CHUNKING"
    )

    print(
        "=" * 70
    )

    print(
        f"Original documents : "
        f"{len(documents)}"
    )

    print(
        f"Generated chunks   : "
        f"{len(chunks)}"
    )

    print(
        f"Chunk size         : "
        f"{CHUNK_SIZE}"
    )

    print(
        f"Chunk overlap      : "
        f"{CHUNK_OVERLAP}"
    )

    return chunks


# ============================================================
# STEP 5 — ADD CHUNK METADATA
# ============================================================

def enrich_metadata(chunks):
    """
    Add deterministic chunk indexes
    and UUIDs.
    """

    counters = {}

    for chunk in chunks:

        source = chunk.metadata[
            "source"
        ]

        if source not in counters:

            counters[source] = 0

        chunk_index = counters[
            source
        ]

        chunk.metadata[
            "chunk_index"
        ] = chunk_index

        chunk_id_string = (
            f"{source}:{chunk_index}"
        )

        chunk_id = str(
            uuid5(
                NAMESPACE_URL,
                chunk_id_string,
            )
        )

        chunk.metadata[
            "chunk_id"
        ] = chunk_id

        counters[
            source
        ] += 1

    return chunks


# ============================================================
# STEP 6 — SHOW CHUNK EXAMPLES
# ============================================================

def show_chunk_examples(
    chunks,
    number=5,
):
    """Display a few chunks for inspection."""

    print(
        "\n" + "=" * 70
    )

    print(
        "CHUNK EXAMPLES"
    )

    print(
        "=" * 70
    )

    for i, chunk in enumerate(
        chunks[:number]
    ):

        print(
            f"\n--- Chunk {i} ---"
        )

        print(
            f"Source      : "
            f"{chunk.metadata.get('source')}"
        )

        print(
            f"Document    : "
            f"{chunk.metadata.get('document_type')}"
        )

        print(
            f"Project     : "
            f"{chunk.metadata.get('project')}"
        )

        print(
            f"Chunk index : "
            f"{chunk.metadata.get('chunk_index')}"
        )

        print(
            f"Chunk ID     : "
            f"{chunk.metadata.get('chunk_id')}"
        )

        print(
            "\nText:"
        )

        print(
            chunk.page_content[:500]
        )


# ============================================================
# STEP 7 — GENERATE GEMINI EMBEDDINGS
# ============================================================
import time

from google.api_core.exceptions import ResourceExhausted


def generate_embeddings(chunks):

    print("\n" + "=" * 70)
    print("GENERATING GEMINI EMBEDDINGS")
    print("=" * 70)

    print(
        f"Model      : {EMBEDDING_MODEL_NAME}"
    )

    print(
        f"Dimensions : {EMBEDDING_DIMENSION}"
    )

    embedding_model = get_embedding_model()

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    print(
        f"Texts to embed: {len(texts)}"
    )

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------

    batch_size = 20

    max_retries = 5

    retry_delay = 10

    embeddings = []

    total = len(texts)

    # --------------------------------------------------------
    # Process batches
    # --------------------------------------------------------

    for start in range(
        0,
        total,
        batch_size,
    ):

        batch = texts[
            start:start + batch_size
        ]

        end = min(
            start + batch_size,
            total,
        )

        print(
            f"\nEmbedding "
            f"{start + 1}-{end}/{total}"
        )

        # ----------------------------------------------------
        # Retry on quota errors
        # ----------------------------------------------------

        for attempt in range(
            max_retries
        ):

            try:

                batch_embeddings = (
                    embedding_model.embed_documents(
                        batch
                    )
                )

                embeddings.extend(
                    batch_embeddings
                )

                print(
                    f"Success: "
                    f"{len(embeddings)}/{total}"
                )

                break

            except Exception as error:

                error_text = str(error)

                if (
                    "429" not in error_text
                    and
                    "RESOURCE_EXHAUSTED"
                    not in error_text
                ):

                    raise

                if attempt == (
                    max_retries - 1
                ):

                    raise RuntimeError(
                        "Gemini embedding quota "
                        "was exceeded after "
                        f"{max_retries} retries."
                    ) from error

                wait_time = (
                    retry_delay
                    * (attempt + 1)
                )

                print(
                    f"Rate limit reached."
                )

                print(
                    f"Waiting "
                    f"{wait_time}s..."
                )

                time.sleep(
                    wait_time
                )

        # ----------------------------------------------------
        # Small delay between batches
        # ----------------------------------------------------

        time.sleep(2)

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------

    if len(embeddings) != total:

        raise ValueError(
            f"Expected {total} embeddings, "
            f"got {len(embeddings)}"
        )

    actual_dimension = len(
        embeddings[0]
    )

    if actual_dimension != (
        EMBEDDING_DIMENSION
    ):

        raise ValueError(
            f"Expected "
            f"{EMBEDDING_DIMENSION} dimensions, "
            f"got {actual_dimension}"
        )

    print("\n" + "=" * 70)
    print("EMBEDDING GENERATION COMPLETE")
    print("=" * 70)

    print(
        f"Embeddings: {len(embeddings)}"
    )

    print(
        f"Dimension : {actual_dimension}"
    )

    return embeddings
# ============================================================
# STEP 8 — BUILD SUPABASE ROWS
# ============================================================

def build_rows(
    chunks,
    embeddings,
):
    """Create rows compatible with Supabase."""

    if len(chunks) != len(
        embeddings
    ):

        raise ValueError(
            "Number of chunks and embeddings "
            "does not match."
        )

    rows = []

    for chunk, embedding in zip(
        chunks,
        embeddings,
    ):

        row = {
            "chunk_id": chunk.metadata[
                "chunk_id"
            ],

            "content": chunk.page_content,

            "metadata": chunk.metadata,

            "embedding": embedding,
        }

        rows.append(
            row
        )

    return rows


# ============================================================
# STEP 9 — CLEAR OLD EMBEDDINGS
# ============================================================

def clear_old_documents():
    """
    Delete the previous RAG vectors.

    IMPORTANT:
    This is necessary because the embedding model
    has changed from BGE to Gemini Embedding 2.
    """

    print(
        "\n" + "=" * 70
    )

    print(
        "CLEARING OLD RAG DATA"
    )

    print(
        "=" * 70
    )

    response = (
        supabase
        .table(TABLE_NAME)
        .delete()
        .neq(
            "chunk_id",
            "00000000-0000-0000-0000-000000000000",
        )
        .execute()
    )

    print(
        "Old RAG documents removed."
    )


# ============================================================
# STEP 10 — STORE DOCUMENTS
# ============================================================

def store_documents(rows):
    """Upload Gemini embeddings and metadata."""

    print(
        "\n" + "=" * 70
    )

    print(
        "SUPABASE STORAGE"
    )

    print(
        "=" * 70
    )

    if not rows:

        print(
            "No rows to insert."
        )

        return

    batch_size = 50

    total = len(rows)

    for start in range(
        0,
        total,
        batch_size,
    ):

        batch = rows[
            start:start + batch_size
        ]

        end = min(
            start + batch_size,
            total,
        )

        print(
            f"Uploading "
            f"{start + 1}-{end}/{total}"
        )

        (
            supabase
            .table(TABLE_NAME)
            .insert(batch)
            .execute()
        )

    print(
        f"\nStored chunks: {total}"
    )

    print(
        f"Embedding model: "
        f"{EMBEDDING_MODEL_NAME}"
    )

    print(
        f"Embedding dimension: "
        f"{EMBEDDING_DIMENSION}"
    )


# ============================================================
# STEP 11 — VERIFY SUPABASE
# ============================================================

def verify_collection():
    """Verify the number of stored documents."""

    response = (
        supabase
        .table(TABLE_NAME)
        .select(
            "id",
            count="exact",
        )
        .execute()
    )

    count = (
        response.count or 0
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "SUPABASE VERIFICATION"
    )

    print(
        "=" * 70
    )

    print(
        f"Table      : "
        f"{TABLE_NAME}"
    )

    print(
        f"Documents  : "
        f"{count}"
    )

    print(
        f"Model      : "
        f"{EMBEDDING_MODEL_NAME}"
    )

    print(
        f"Dimensions : "
        f"{EMBEDDING_DIMENSION}"
    )


# ============================================================
# STEP 12 — MAIN PIPELINE
# ============================================================

def main():

    print("\n")

    print(
        "=" * 70
    )

    print(
        "PERSONAL PROFILE RAG"
    )

    print(
        "SUPABASE INGESTION PIPELINE"
    )

    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # 1. Verify API key
    # --------------------------------------------------------

    if not os.getenv(
        "GOOGLE_API_KEY"
    ):

        raise RuntimeError(
            "GOOGLE_API_KEY environment "
            "variable is not set."
        )

    print(
        "\nGemini API key: OK"
    )

    # --------------------------------------------------------
    # 2. Find files
    # --------------------------------------------------------

    files = (
        find_markdown_files()
    )

    if not files:

        print(
            "\nNo Markdown files found."
        )

        return

    # --------------------------------------------------------
    # 3. Load documents
    # --------------------------------------------------------

    documents = (
        load_documents(files)
    )

    if not documents:

        print(
            "\nNo documents loaded."
        )

        return

    # --------------------------------------------------------
    # 4. Split documents
    # --------------------------------------------------------

    chunks = (
        split_documents(documents)
    )

    if not chunks:

        print(
            "\nNo chunks generated."
        )

        return

    # --------------------------------------------------------
    # 5. Add metadata
    # --------------------------------------------------------

    chunks = (
        enrich_metadata(chunks)
    )

    # --------------------------------------------------------
    # 6. Show examples
    # --------------------------------------------------------

    show_chunk_examples(
        chunks
    )

    # --------------------------------------------------------
    # 7. Generate Gemini embeddings
    # --------------------------------------------------------

    embeddings = (
        generate_embeddings(
            chunks
        )
    )

    # --------------------------------------------------------
    # 8. Build database rows
    # --------------------------------------------------------

    rows = build_rows(
        chunks,
        embeddings,
    )

    # --------------------------------------------------------
    # 9. Clear old BGE vectors
    # --------------------------------------------------------

    clear_old_documents()

    # --------------------------------------------------------
    # 10. Store Gemini vectors
    # --------------------------------------------------------

    store_documents(
        rows
    )

    # --------------------------------------------------------
    # 11. Verify
    # --------------------------------------------------------

    verify_collection()

    # --------------------------------------------------------
    # DONE
    # --------------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "INGESTION COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        f"\nModel: "
        f"{EMBEDDING_MODEL_NAME}"
    )

    print(
        f"Dimension: "
        f"{EMBEDDING_DIMENSION}"
    )

    print(
        f"Chunks: "
        f"{len(chunks)}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()