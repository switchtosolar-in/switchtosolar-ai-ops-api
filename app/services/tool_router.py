import json
from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


ALLOWED_OPERATION_TOOLS = [
    "get_active_cities_count",
    "get_active_installers_count",
    "get_recent_reports_count",
    "get_top_report_cities",
    "get_stale_leads_count",
    "get_new_leads_count",
    "get_sla_bucket_summary",
    "get_lead_status_summary",
    "get_report_activity_summary",
    "no_matching_operations_tool",
    "get_latest_installer",
]


def classify_tool(question: str) -> dict:
    system_prompt = """
You are a strict router for an internal SwitchToSolar AI Ops assistant.

Return ONLY valid JSON.

You must classify the user's question into:
- knowledge
- operations
- unsupported

If operations, choose exactly one allowed tool.

Allowed operation tools:
- get_active_cities_count
- get_active_installers_count
- get_recent_reports_count
- get_top_report_cities
- get_stale_leads_count
- get_new_leads_count
- get_sla_bucket_summary
- get_lead_status_summary
- get_report_activity_summary
- no_matching_operations_tool
- get_latest_installer

Rules:
- Do NOT write SQL.
- Do NOT invent tools.
- If user asks about live platform numbers, reports, leads, installers, cities, SLA, activity, summaries, or counts, use operations.
- If user asks how the product/AI/system works, use knowledge.
- If unrelated to SwitchToSolar, use unsupported.
- Extract days/hours when present.
- If the user says "last two months", days = 60.
- If the user says "last 90 days", days = 90.
- If no period is mentioned, days = null and hours = null.
- If user asks latest installer, newest installer, recently onboarded installer, or who was onboarded last, choose get_latest_installer.

JSON format:
{
  "intent": "knowledge | operations | unsupported",
  "tool_name": "tool name or null",
  "days": number or null,
  "hours": number or null,
  "confidence": "high | medium | low"
}
"""

    response = client.chat.completions.create(
        model=settings.OPENAI_CHAT_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )

    raw = response.choices[0].message.content or "{}"

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "intent": "knowledge",
            "tool_name": None,
            "days": None,
            "hours": None,
            "confidence": "low",
        }

    intent = data.get("intent")
    tool_name = data.get("tool_name")

    if intent not in ["knowledge", "operations", "unsupported"]:
        intent = "knowledge"

    if intent == "operations" and tool_name not in ALLOWED_OPERATION_TOOLS:
        tool_name = "no_matching_operations_tool"

    return {
        "intent": intent,
        "tool_name": tool_name,
        "days": data.get("days"),
        "hours": data.get("hours"),
        "confidence": data.get("confidence", "medium"),
    }