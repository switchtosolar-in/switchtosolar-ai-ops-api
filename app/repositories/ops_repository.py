from app.db.mssql import get_mssql_connection


def get_active_cities_count() -> int:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM dbo.cities
            WHERE is_active = 1;
        """)
        row = cursor.fetchone()
        return int(row.total or 0)


def get_active_installers_count() -> int:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM dbo.installers
            WHERE is_active = 1
              AND is_archived = 0;
        """)
        row = cursor.fetchone()
        return int(row.total or 0)


def get_recent_reports_count(days: int = 7) -> int:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM dbo.solar_reports
            WHERE created_at >= DATEADD(DAY, ?, SYSUTCDATETIME());
        """, -abs(days))
        row = cursor.fetchone()
        return int(row.total or 0)


def get_top_report_cities(days: int = 30, limit: int = 5) -> list[dict]:
    safe_limit = max(1, min(limit, 10))

    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT TOP ({safe_limit})
                ISNULL(NULLIF(LTRIM(RTRIM(city)), ''), 'Unknown') AS city,
                COUNT(*) AS total_reports
            FROM dbo.solar_reports
            WHERE created_at >= DATEADD(DAY, ?, SYSUTCDATETIME())
            GROUP BY ISNULL(NULLIF(LTRIM(RTRIM(city)), ''), 'Unknown')
            ORDER BY total_reports DESC;
        """, -abs(days))

        rows = cursor.fetchall()

    return [
        {
            "city": row.city,
            "total_reports": int(row.total_reports or 0),
        }
        for row in rows
    ]


def get_stale_leads_count(hours: int = 24) -> int:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM dbo.leads
            WHERE is_deleted = 0
              AND installer_id IS NOT NULL
              AND LOWER(ISNULL(lead_status, 'new')) = 'new'
              AND submitted_at <= DATEADD(HOUR, ?, SYSUTCDATETIME());
        """, -abs(hours))

        row = cursor.fetchone()
        return int(row.total or 0)


def get_new_leads_count(hours: int = 24) -> int:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM dbo.leads
            WHERE is_deleted = 0
              AND submitted_at >= DATEADD(HOUR, ?, SYSUTCDATETIME());
        """, -abs(hours))

        row = cursor.fetchone()
        return int(row.total or 0)


def get_sla_bucket_summary() -> dict:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                SUM(CASE
                    WHEN submitted_at <= DATEADD(HOUR, -12, SYSUTCDATETIME())
                     AND submitted_at >  DATEADD(HOUR, -24, SYSUTCDATETIME())
                    THEN 1 ELSE 0 END
                ) AS leads_12_to_24h,

                SUM(CASE
                    WHEN submitted_at <= DATEADD(HOUR, -24, SYSUTCDATETIME())
                     AND submitted_at >  DATEADD(HOUR, -36, SYSUTCDATETIME())
                    THEN 1 ELSE 0 END
                ) AS leads_24_to_36h,

                SUM(CASE
                    WHEN submitted_at <= DATEADD(HOUR, -36, SYSUTCDATETIME())
                    THEN 1 ELSE 0 END
                ) AS leads_36h_plus

            FROM dbo.leads
            WHERE is_deleted = 0
              AND installer_id IS NOT NULL
              AND LOWER(ISNULL(lead_status, 'new')) = 'new';
        """)

        row = cursor.fetchone()

    return {
        "leads_12_to_24h": int(row.leads_12_to_24h or 0),
        "leads_24_to_36h": int(row.leads_24_to_36h or 0),
        "leads_36h_plus": int(row.leads_36h_plus or 0),
    }

def get_lead_status_summary(days: int = 30) -> list[dict]:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                LOWER(ISNULL(lead_status, 'unknown')) AS lead_status,
                COUNT(*) AS total
            FROM dbo.leads
            WHERE is_deleted = 0
              AND submitted_at >= DATEADD(DAY, ?, SYSUTCDATETIME())
            GROUP BY LOWER(ISNULL(lead_status, 'unknown'))
            ORDER BY total DESC;
        """, -abs(days))

        rows = cursor.fetchall()

    return [
        {
            "lead_status": row.lead_status,
            "total": int(row.total or 0),
        }
        for row in rows
    ]


def get_report_activity_summary(days: int = 30) -> dict:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) AS total_reports,
                COUNT(DISTINCT ISNULL(NULLIF(LTRIM(RTRIM(city)), ''), 'Unknown')) AS unique_cities,
                ISNULL(AVG(CAST(bill AS FLOAT)), 0) AS avg_monthly_bill
            FROM dbo.solar_reports
            WHERE created_at >= DATEADD(DAY, ?, SYSUTCDATETIME());
        """, -abs(days))

        row = cursor.fetchone()

    return {
        "total_reports": int(row.total_reports or 0),
        "unique_cities": int(row.unique_cities or 0),
        "avg_monthly_bill": round(float(row.avg_monthly_bill or 0), 2),
    }

def get_latest_installer() -> dict | None:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TOP 1
                id,
                name,
                city,
                state,
                is_active,
                is_verified,
                kyc_status,
                publish_state,
                account_status,
                created_at,
                application_submitted_at
            FROM dbo.installers
            WHERE is_archived = 0
            ORDER BY
                COALESCE(application_submitted_at, created_at) DESC,
                id DESC;
        """)

        row = cursor.fetchone()

    if not row:
        return None

    return {
        "id": int(row.id),
        "name": row.name,
        "city": row.city,
        "state": row.state,
        "is_active": bool(row.is_active),
        "is_verified": bool(row.is_verified),
        "kyc_status": row.kyc_status,
        "publish_state": row.publish_state,
        "account_status": row.account_status,
        "created_at": str(row.created_at) if row.created_at else None,
        "application_submitted_at": str(row.application_submitted_at) if row.application_submitted_at else None,
    }