from typing import List, Dict


def _format_sources(chunks: List[Dict]) -> str:
    """
    Formats sources for the prompt so the LLM can cite them.
    """
    lines = []
    for i, ch in enumerate(chunks, start=1):
        lines.append(
            f"[{i}] {ch['document_title']} (chunk {ch['chunk_index']})"
        )
    return "\n".join(lines)


def _format_context(chunks: List[Dict]) -> str:
    """
    Formats retrieved chunks into a single context string.
    """
    blocks = []
    for i, ch in enumerate(chunks, start=1):
        blocks.append(
            f"[{i}] SOURCE: {ch['document_title']} (chunk {ch['chunk_index']})\n"
            f"{ch['chunk_text']}"
        )
    return "\n\n---\n\n".join(blocks)


def build_prompt(question: str, chunks: List[Dict]) -> Dict:
    """
    Builds a structured prompt for the LLM.

    Returns:
        {
            "system": "...",
            "user": "..."
        }
    """
    if not chunks:
        # Edge case: no context found
        system_prompt = (
            "You are an AI assistant. If no context is provided, say you don't have enough information."
        )
        user_prompt = f"Question: {question}"
        return {"system": system_prompt, "user": user_prompt}

    context_text = _format_context(chunks)
    sources_text = _format_sources(chunks)

    system_prompt = (
        "You are an AI assistant for SwitchToSolar.\n"
        "Answer ONLY using the provided context.\n"
        "Do NOT make up information.\n"
        "If the answer is not in the context, say you don't know.\n"
        "Be clear, concise, and structured.\n"
        "Always include source references like [1], [2]."
    )

    user_prompt = (
        f"Question:\n{question}\n\n"
        f"Context:\n{context_text}\n\n"
        f"Sources:\n{sources_text}\n\n"
        "Answer:"
    )

    return {
        "system": system_prompt,
        "user": user_prompt,
    }