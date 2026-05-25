from app.services.ops_service import extract_days, extract_hours


def test_extract_days_last_two_months():
    assert extract_days("Give me report activity summary for last two months") == 60


def test_extract_days_last_90_days():
    assert extract_days("Give me lead status summary for last 90 days") == 90


def test_extract_days_last_month():
    assert extract_days("How many reports generated last month?") == 30


def test_extract_hours_last_30_days():
    assert extract_hours("How many new leads in last 30 days?") == 720


def test_extract_hours_last_24_hours():
    assert extract_hours("How many new leads in last 24 hours?") == 24



from unittest.mock import patch

from app.services.ops_service import answer_operations_question


@patch("app.services.ops_service.get_report_activity_summary")
def test_report_activity_summary_uses_correct_tool(mock_summary):
    mock_summary.return_value = {
        "total_reports": 161,
        "unique_cities": 9,
        "avg_monthly_bill": 5746.58,
    }

    response = answer_operations_question("Give me report activity summary for last two months")

    assert response["tool"] == "get_report_activity_summary"
    assert response["data"]["days"] == 60
    assert response["data"]["total_reports"] == 161


@patch("app.services.ops_service.get_recent_reports_count")
def test_recent_reports_count_uses_correct_tool(mock_count):
    mock_count.return_value = 25

    response = answer_operations_question("How many reports generated in last 30 days?")

    assert response["tool"] == "get_recent_reports_count"
    assert response["data"]["days"] == 30
    assert response["data"]["recent_reports"] == 25


@patch("app.services.ops_service.get_lead_status_summary")
def test_lead_status_summary_uses_correct_tool(mock_statuses):
    mock_statuses.return_value = [
        {"lead_status": "new", "total": 25},
        {"lead_status": "unlocked", "total": 8},
    ]

    response = answer_operations_question("Give me lead status summary for last 90 days")

    assert response["tool"] == "get_lead_status_summary"
    assert response["data"]["days"] == 90
    assert response["data"]["statuses"][0]["lead_status"] == "new"


@patch("app.services.ops_service.get_top_report_cities")
def test_top_report_cities_uses_correct_tool(mock_cities):
    mock_cities.return_value = [
        {"city": "Hyderabad", "total_reports": 40},
        {"city": "Bengaluru", "total_reports": 20},
    ]

    response = answer_operations_question("What are top report cities for last 30 days?")

    assert response["tool"] == "get_top_report_cities"
    assert response["data"]["days"] == 30
    assert response["data"]["cities"][0]["city"] == "Hyderabad"