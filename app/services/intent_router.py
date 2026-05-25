def classify_intent(question: str) -> str:
    """
    Classifies the user's question into one of:
    - knowledge
    - operations
    - unsupported

    Rule-based for safety and control.
    """
    normalized = question.lower().strip()

    unsupported_keywords = [
        "weather",
        "stock price",
        "cricket",
        "movie",
        "recipe",
        "joke",
        "politics",
    ]

    operations_keywords = [
        "how many leads",
        "stale leads",
        "pending leads",
        "overdue leads",
        "new leads",
        "leads today",
        "lead count",
        "last 24",
        "last 7",
        "last 30",
        "last month",
        "last two months",
        "last 2 months",
        "sla",
        "installer activity",
        "active installer",
        "active installers",
        "how many installers",
        "installer count",
        "city report",
        "active cities",
        "how many cities",
        "city count",
        "reports today",
        "reports generated",
        "report generated",
        "solar reports",
        "report submissions",
        "top city",
        "top cities",
        "top report cities",
        "report cities",
        "which city",
        "most report",
        "most reports",
        "most submission",
        "most submissions",
        "payments",
        "revenue",
        "unlocked leads",
        "leads pending",
        "which installers",
        "lead status",
        "leads by status",
        "status summary",
        "report activity",
        "report summary",
        "reports summary",
    ]

    for keyword in unsupported_keywords:
        if keyword in normalized:
            return "unsupported"

    for keyword in operations_keywords:
        if keyword in normalized:
            return "operations"

    return "knowledge"