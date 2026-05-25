# AI Advisor Design

The AI Advisor is a chatbot-like feature that answers user questions based on their solar report.

Key design principles:

- Context-aware responses using report data
- Strict guardrails to avoid hallucination
- Refusal logic if question is outside scope
- Structured prompts with system and user roles

The AI Advisor only answers questions related to the user’s solar report and does not generate generic or unrelated responses.

It uses OpenAI models and includes retry and fallback logic.
