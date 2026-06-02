"""
LLM service for AI Ops response generation.

This file owns the direct chat model call.

Structured prompt
  -> OpenAI chat model
  -> generated answer
  -> model metadata

Keeping this logic isolated makes the RAG orchestration layer cleaner and
keeps model/provider integration separate from retrieval and logging logic.
"""

from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_answer(system_prompt: str, user_prompt: str) -> dict:
    """
    Sends structured prompt to OpenAI chat model and returns answer metadata.
    """
    response = client.chat.completions.create(
        model=settings.OPENAI_CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "model": settings.OPENAI_CHAT_MODEL,
    }