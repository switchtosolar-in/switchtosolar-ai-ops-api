from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def create_embedding(text: str) -> list[float]:
    """
    Converts text into a vector embedding using OpenAI.
    """
    if not text.strip():
        raise ValueError("Cannot create embedding for empty text.")

    response = client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding