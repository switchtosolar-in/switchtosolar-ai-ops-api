"""
Operational AI service.

This file maps operational questions to predefined backend tools.

User/Admin question
  -> routed tool decision
  -> safe service handler
  -> repository function
  -> deterministic operational response

The service intentionally avoids AI-generated SQL. The model may help route
the question, but live platform data is retrieved only through approved
repository functions.
"""


import re

from app.repositories.ops_repository import (
    get_active_cities_count,
    get_active_installers_count,
    get_recent_reports_count,
    get_top_report_cities,
    get_stale_leads_count,
    get_new_leads_count,
    get_sla_bucket_summary,
    get_lead_status_summary,
    get_report_activity_summary,
    get_latest_installer,
)


def extract_days(question: str, default_days: int = 7) -> int:
    normalized = question.lower().strip()

    if "today" in normalized:
        return 1

    if "last 24" in normalized or "24 hours" in normalized:
        return 1

    if "last 7" in normalized or "7 days" in normalized or "week" in normalized:
        return 7

    if "last 30" in normalized or "30 days" in normalized or "last month" in normalized:
        return 30

    if "last two months" in normalized or "last 2 months" in normalized or "two months" in normalized:
        return 60

    match = re.search(r"last\s+(\d+)\s+days?", normalized)
    if match:
        return max(1, min(int(match.group(1)), 365))

    match = re.search(r"last\s+(\d+)\s+months?", normalized)
    if match:
        return max(1, min(int(match.group(1)) * 30, 365))

    return default_days


def extract_hours(question: str, default_hours: int = 24) -> int:
    normalized = question.lower().strip()

    if "last 24" in normalized or "24 hours" in normalized:
        return 24

    if "last 30 days" in normalized or "30 days" in normalized or "last month" in normalized:
        return 30 * 24

    if "last two months" in normalized or "last 2 months" in normalized or "two months" in normalized:
        return 60 * 24

    match = re.search(r"last\s+(\d+)\s+hours?", normalized)
    if match:
        return max(1, min(int(match.group(1)), 24 * 365))

    match = re.search(r"last\s+(\d+)\s+days?", normalized)
    if match:
        return max(1, min(int(match.group(1)) * 24, 24 * 365))

    match = re.search(r"last\s+(\d+)\s+months?", normalized)
    if match:
        return max(1, min(int(match.group(1)) * 30 * 24, 24 * 365))

    return default_hours


def answer_operations_question(question: str, route_decision: dict | None = None) -> dict:
    """
    Maps operations questions to predefined read-only MSSQL tools.

    Deterministic first version:
    - no free-form SQL
    - no LLM call
    - no write operations
    """
    normalized = question.lower().strip()

    routed_tool = route_decision.get("tool_name") if route_decision else None
    routed_days = route_decision.get("days") if route_decision else None
    routed_hours = route_decision.get("hours") if route_decision else None

    if routed_tool == "get_lead_status_summary":
        days = int(routed_days or extract_days(question, default_days=30))
        statuses = get_lead_status_summary(days=days)

        lines = [
            f"- {item['lead_status']}: {item['total']} leads"
            for item in statuses
        ]

        return {
            "answer": f"Lead status summary for the last {days} days:\n" + "\n".join(lines),
            "tool": "get_lead_status_summary",
            "data": {"days": days, "statuses": statuses},
        }

    if routed_tool == "get_report_activity_summary":
        days = int(routed_days or extract_days(question, default_days=30))
        summary = get_report_activity_summary(days=days)

        return {
            "answer": (
                f"Report activity summary for the last {days} days:\n"
                f"- Total reports: {summary['total_reports']}\n"
                f"- Unique cities: {summary['unique_cities']}\n"
                f"- Average monthly bill: ₹{summary['avg_monthly_bill']}"
            ),
            "tool": "get_report_activity_summary",
            "data": {"days": days, **summary},
        }

    if routed_tool == "get_active_cities_count":
        count = get_active_cities_count()
        return {
            "answer": f"There are {count} active cities in SwitchToSolar.",
            "tool": "get_active_cities_count",
            "data": {"active_cities": count},
        }

    if routed_tool == "get_active_installers_count":
        count = get_active_installers_count()
        return {
            "answer": f"There are {count} active installers in SwitchToSolar.",
            "tool": "get_active_installers_count",
            "data": {"active_installers": count},
        }

    if routed_tool == "get_recent_reports_count":
        days = int(routed_days or extract_days(question, default_days=7))
        count = get_recent_reports_count(days=days)
        return {
            "answer": f"{count} solar reports were generated in the last {days} days.",
            "tool": "get_recent_reports_count",
            "data": {"days": days, "recent_reports": count},
        }

    if routed_tool == "get_top_report_cities":
        days = int(routed_days or extract_days(question, default_days=30))
        cities = get_top_report_cities(days=days, limit=5)
        lines = [
            f"{index + 1}. {item['city']} — {item['total_reports']} reports"
            for index, item in enumerate(cities)
        ]

        return {
            "answer": f"Top cities by solar report submissions in the last {days} days:\n" + "\n".join(lines),
            "tool": "get_top_report_cities",
            "data": {"days": days, "cities": cities},
        }

    if routed_tool == "get_new_leads_count":
        hours = int(routed_hours or extract_hours(question, default_hours=24))
        count = get_new_leads_count(hours=hours)
        period = f"{hours // 24} days" if hours % 24 == 0 else f"{hours} hours"
        return {
            "answer": f"{count} new leads were submitted in the last {period}.",
            "tool": "get_new_leads_count",
            "data": {"hours": hours, "new_leads": count},
        }

    if routed_tool == "get_stale_leads_count":
        hours = int(routed_hours or extract_hours(question, default_hours=24))
        count = get_stale_leads_count(hours=hours)
        period = f"{hours // 24} days" if hours % 24 == 0 else f"{hours} hours"
        return {
            "answer": f"There are {count} stale leads older than {period} that are still in new status.",
            "tool": "get_stale_leads_count",
            "data": {"hours": hours, "stale_leads": count},
        }

    if routed_tool == "get_sla_bucket_summary":
        summary = get_sla_bucket_summary()
        return {
            "answer": (
                "Current SLA lead aging summary:\n"
                f"- 12–24 hours: {summary['leads_12_to_24h']} leads\n"
                f"- 24–36 hours: {summary['leads_24_to_36h']} leads\n"
                f"- 36+ hours: {summary['leads_36h_plus']} leads"
            ),
            "tool": "get_sla_bucket_summary",
            "data": summary,
        }

    if routed_tool == "no_matching_operations_tool":
        return {
            "answer": (
                "This is an operations question, but I do not yet have a predefined safe tool "
                "for this exact request."
            ),
            "tool": "no_matching_operations_tool",
            "data": {},
        }

    if routed_tool == "get_latest_installer":
        installer = get_latest_installer()

        if not installer:
            return {
                "answer": "No installer records were found.",
                "tool": "get_latest_installer",
                "data": {"installer": None},
            }

        return {
            "answer": (
                "Latest installer onboarded:\n"
                f"- Name: {installer['name']}\n"
                f"- City: {installer['city'] or 'Unknown'}\n"
                f"- State: {installer['state'] or 'Unknown'}\n"
                f"- Active: {'Yes' if installer['is_active'] else 'No'}\n"
                f"- Verified: {'Yes' if installer['is_verified'] else 'No'}\n"
                f"- KYC status: {installer['kyc_status']}\n"
                f"- Publish state: {installer['publish_state']}\n"
                f"- Account status: {installer['account_status']}\n"
                f"- Submitted at: {installer['application_submitted_at'] or installer['created_at']}"
            ),
            "tool": "get_latest_installer",
            "data": {"installer": installer},
        }
   

   # Fallback keyword routing.
# This keeps operations usable if the router returns no tool or a low-confidence result.

    if "lead status" in normalized or "leads by status" in normalized or "status summary" in normalized:
        days = extract_days(question, default_days=30)
        statuses = get_lead_status_summary(days=days)

        if not statuses:
            return {
                "answer": f"No leads were found in the last {days} days.",
                "tool": "get_lead_status_summary",
                "data": {"days": days, "statuses": []},
            }

        lines = [
            f"- {item['lead_status']}: {item['total']} leads"
            for item in statuses
        ]

        return {
            "answer": f"Lead status summary for the last {days} days:\n" + "\n".join(lines),
            "tool": "get_lead_status_summary",
            "data": {"days": days, "statuses": statuses},
        }

    if "report activity" in normalized or "report summary" in normalized or "reports summary" in normalized:
        days = extract_days(question, default_days=30)
        summary = get_report_activity_summary(days=days)

        return {
            "answer": (
                f"Report activity summary for the last {days} days:\n"
                f"- Total reports: {summary['total_reports']}\n"
                f"- Unique cities: {summary['unique_cities']}\n"
                f"- Average monthly bill: ₹{summary['avg_monthly_bill']}"
            ),
            "tool": "get_report_activity_summary",
            "data": {"days": days, **summary},
        }

    # 2. Entity count tools
    if "active cit" in normalized or "how many cities" in normalized or "city count" in normalized:
        count = get_active_cities_count()

        return {
            "answer": f"There are {count} active cities in SwitchToSolar.",
            "tool": "get_active_cities_count",
            "data": {"active_cities": count},
        }

    if "active installer" in normalized or "how many installers" in normalized or "installer count" in normalized:
        count = get_active_installers_count()

        return {
            "answer": f"There are {count} active installers in SwitchToSolar.",
            "tool": "get_active_installers_count",
            "data": {"active_installers": count},
        }

    # 3. Specific report ranking tools
    if (
        "top report cities" in normalized
        or "report cities" in normalized
        or "top city" in normalized
        or "top cities" in normalized
        or "most report" in normalized
        or "most submission" in normalized
        or "which city" in normalized
    ):
        days = extract_days(question, default_days=30)
        cities = get_top_report_cities(days=days, limit=5)

        if not cities:
            return {
                "answer": f"There are no report submissions found in the last {days} days.",
                "tool": "get_top_report_cities",
                "data": {"days": days, "cities": []},
            }

        lines = [
            f"{index + 1}. {item['city']} — {item['total_reports']} reports"
            for index, item in enumerate(cities)
        ]

        return {
            "answer": f"Top cities by solar report submissions in the last {days} days:\n" + "\n".join(lines),
            "tool": "get_top_report_cities",
            "data": {"days": days, "cities": cities},
        }

    # 4. Lead aging tools
    if "stale" in normalized or "overdue" in normalized:
        hours = extract_hours(question, default_hours=24)
        count = get_stale_leads_count(hours=hours)

        if hours % 24 == 0:
            period = f"{hours // 24} days"
        else:
            period = f"{hours} hours"

        return {
            "answer": f"There are {count} stale leads older than {period} that are still in new status.",
            "tool": "get_stale_leads_count",
            "data": {"hours": hours, "stale_leads": count},
        }

    if "new lead" in normalized or "leads today" in normalized or "last 24" in normalized or "lead count" in normalized:
        hours = extract_hours(question, default_hours=24)
        count = get_new_leads_count(hours=hours)

        if hours % 24 == 0:
            period = f"{hours // 24} days"
        else:
            period = f"{hours} hours"

        return {
            "answer": f"{count} new leads were submitted in the last {period}.",
            "tool": "get_new_leads_count",
            "data": {"hours": hours, "new_leads": count},
        }

    if "sla" in normalized:
        summary = get_sla_bucket_summary()

        return {
            "answer": (
                "Current SLA lead aging summary:\n"
                f"- 12–24 hours: {summary['leads_12_to_24h']} leads\n"
                f"- 24–36 hours: {summary['leads_24_to_36h']} leads\n"
                f"- 36+ hours: {summary['leads_36h_plus']} leads\n\n"
                "This means these are assigned leads still in new status, grouped by how long they have been waiting."
            ),
            "tool": "get_sla_bucket_summary",
            "data": summary,
        }

    # 5. Generic report count tool comes after specific report tools
    if "report" in normalized or "solar report" in normalized or "generated" in normalized:
        days = extract_days(question, default_days=7)
        count = get_recent_reports_count(days=days)

        return {
            "answer": f"{count} solar reports were generated in the last {days} days.",
            "tool": "get_recent_reports_count",
            "data": {"days": days, "recent_reports": count},
        }

    return {
        "answer": (
            "This is an operations question, but I do not yet have a predefined safe tool "
            "for this exact request."
        ),
        "tool": "no_matching_operations_tool",
        "data": {},
    }