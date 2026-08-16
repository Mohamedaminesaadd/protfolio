import os

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
)


EMBEDDING_MODEL = "gemini-embedding-2"

EMBEDDING_DIMENSION = 768


def get_embedding_model():

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is not set."
        )

    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=api_key,
        output_dimensionality=EMBEDDING_DIMENSION,
    )