def chunk_text(text: str, max_chars: int = 800, overlap: int = 120) -> list[str]:
    """
    Splits long text into smaller overlapping chunks.

    max_chars:
        Maximum characters per chunk.

    overlap:
        Number of characters repeated between chunks to preserve context.
    """
    cleaned_text = " ".join(text.split())

    if not cleaned_text:
        return []

    chunks = []
    start = 0

    while start < len(cleaned_text):
        end = start + max_chars
        chunk = cleaned_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start < 0:
            start = 0

        if start >= len(cleaned_text):
            break

    return chunks


def chunk_document(document: dict, max_chars: int = 800, overlap: int = 120) -> list[dict]:
    """
    Converts one document into structured chunks.
    """
    raw_chunks = chunk_text(
        text=document["content"],
        max_chars=max_chars,
        overlap=overlap,
    )

    return [
        {
            "title": document["title"],
            "source_path": document["source_path"],
            "chunk_index": index,
            "chunk_text": chunk,
        }
        for index, chunk in enumerate(raw_chunks)
    ]