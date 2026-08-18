from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI
from sqlalchemy import select

from inframonitor_api.database import SessionLocal, check_database
from inframonitor_api.models import Host, Report

app = FastAPI(
    title="InfraMonitor API",
    version="0.1.0",
)


@app.get("/health")
def health():
    database_ok = check_database()

    return {
        "status": "ok",
        "database": "connected" if database_ok else "disconnected",
    }


@app.post("/api/v1/reports")
def receive_report(report: dict[str, Any]):
    hostname = report.get("system", {}).get("hostname")

    if not hostname:
        return {
            "status": "error",
            "message": "Missing hostname",
        }

    now = datetime.now(UTC)

    with SessionLocal() as session:
        host = session.scalar(
            select(Host).where(Host.hostname == hostname)
        )

        if host is None:
            host = Host(
                hostname=hostname,
                first_seen=now,
                last_seen=now,
            )

            session.add(host)
            session.flush()

        else:
            host.last_seen = now

        db_report = Report(
            hostname=hostname,
            host_id=host.id,
            data=report,
        )

        session.add(db_report)
        session.commit()

        report_id = db_report.id

    return {
        "status": "received",
        "hostname": hostname,
        "host_id": host.id,
        "report_id": report_id,
    }


@app.get("/api/v1/reports")
def get_reports():
    with SessionLocal() as session:
        reports = session.scalars(
            select(Report)
            .order_by(Report.received_at.desc())
            .limit(100)
        ).all()

        return [
            {
                "id": report.id,
                "hostname": report.hostname,
                "received_at": report.received_at,
                "data": report.data,
            }
            for report in reports
        ]    


@app.get("/api/v1/hosts/{hostname}/reports")
def get_host_reports(hostname: str):
    with SessionLocal() as session:
        reports = session.scalars(
            select(Report)
            .where(Report.hostname == hostname)
            .order_by(Report.received_at.desc())
            .limit(100)
        ).all()

        return [
            {
                "id": report.id,
                "hostname": report.hostname,
                "received_at": report.received_at,
                "data": report.data,
            }
            for report in reports
        ]        