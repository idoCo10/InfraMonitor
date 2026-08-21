from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from inframonitor_api.database import SessionLocal, check_database
from inframonitor_api.models import Host, Report

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


app = FastAPI(
    title="InfraMonitor API",
    version="0.1.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
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


@app.get("/api/v1/hosts")
def get_hosts():
    with SessionLocal() as session:
        hosts = session.scalars(
            select(Host).order_by(Host.hostname)
        ).all()

        return [
            {
                "id": host.id,
                "hostname": host.hostname,
                "first_seen": host.first_seen,
                "last_seen": host.last_seen,
            }
            for host in hosts
        ]        


@app.get("/api/v1/hosts/{hostname}")
def get_host(hostname: str):
    with SessionLocal() as session:
        host = session.scalar(
            select(Host).where(Host.hostname == hostname)
        )

        if host is None:
            raise HTTPException(
                status_code=404,
                detail="Host not found",
            )

        latest_report = session.scalar(
            select(Report)
            .where(Report.host_id == host.id)
            .order_by(Report.received_at.desc())
            .limit(1)
        )

        return {
            "id": host.id,
            "hostname": host.hostname,
            "first_seen": host.first_seen,
            "last_seen": host.last_seen,
            "latest_report": (
                latest_report.data
                if latest_report
                else None
            ),
        }        


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    now = datetime.now(UTC)

    with SessionLocal() as session:
        hosts = session.scalars(
            select(Host).order_by(Host.hostname)
        ).all()

        dashboard_hosts = []

        for host in hosts:
            latest_report = session.scalar(
                select(Report)
                .where(Report.host_id == host.id)
                .order_by(Report.received_at.desc())
                .limit(1)
            )

            report_data = (
                latest_report.data
                if latest_report
                else {}
            )

            system = report_data.get("system", {})
            cpu = report_data.get("cpu", {})
            memory = report_data.get("memory", {}).get("ram", {})

            seconds_since_seen = (
                now - host.last_seen
            ).total_seconds()

            is_online = seconds_since_seen < 30

            dashboard_hosts.append(
                {
                    "hostname": host.hostname,
                    "status": "Online" if is_online else "Offline",
                    "os": system.get("os", "Unknown"),
                    "cpu": cpu.get("utilization_percent"),
                    "memory": memory.get("utilization_percent"),
                    "last_seen": host.last_seen,
                }
            )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "hosts": dashboard_hosts,
        },
    )


@app.get("/hosts/{hostname}", response_class=HTMLResponse)
def host_details(request: Request, hostname: str):
    with SessionLocal() as session:
        host = session.scalar(
            select(Host).where(Host.hostname == hostname)
        )

        if host is None:
            raise HTTPException(
                status_code=404,
                detail="Host not found",
            )

        latest_report = session.scalar(
            select(Report)
            .where(Report.host_id == host.id)
            .order_by(Report.received_at.desc())
            .limit(1)
        )

        report_data = (
            latest_report.data
            if latest_report
            else {}
        )

        seconds_since_seen = (
            datetime.now(UTC) - host.last_seen
        ).total_seconds()

        host_data = {
            "id": host.id,
            "hostname": host.hostname,
            "status": (
                "Online"
                if seconds_since_seen < 30
                else "Offline"
            ),
            "first_seen": host.first_seen,
            "last_seen": host.last_seen,
            "report": report_data,
        }

    return templates.TemplateResponse(
        request=request,
        name="host.html",
        context={
            "host": host_data,
        },
    )    

@app.get("/api/v1/hosts/{hostname}/metrics")
def get_host_metrics(hostname: str):
    with SessionLocal() as session:
        host = session.scalar(
            select(Host).where(Host.hostname == hostname)
        )

        if host is None:
            raise HTTPException(
                status_code=404,
                detail="Host not found",
            )

        reports = session.scalars(
            select(Report)
            .where(Report.host_id == host.id)
            .order_by(Report.received_at.asc())
            .limit(500)
        ).all()

        metrics = []

        for report in reports:
            data = report.data

            metrics.append(
                {
                    "timestamp": report.received_at,
                    "cpu": data.get("cpu", {}).get(
                        "utilization_percent"
                    ),
                    "memory": data.get("memory", {})
                    .get("ram", {})
                    .get("utilization_percent"),
                }
            )

        return metrics    


@app.get("/api/v1/dashboard")
def dashboard_data():
    now = datetime.now(UTC)

    with SessionLocal() as session:
        hosts = session.scalars(
            select(Host).order_by(Host.hostname)
        ).all()

        result = []

        for host in hosts:
            reports = session.scalars(
                select(Report)
                .where(Report.host_id == host.id)
                .order_by(Report.received_at.desc())
                .limit(2)
            ).all()

            latest_report = reports[0] if reports else None

            report_data = (
                latest_report.data
                if latest_report
                else {}
            )

            # Learn reporting interval from last two reports.
            if len(reports) >= 2:
                interval = round(
                    (
                        reports[0].received_at
                        - reports[1].received_at
                    ).total_seconds()
                )
            else:
                interval = 5

            interval = max(interval, 1)

            seconds_since_seen = (
                now - host.last_seen
            ).total_seconds()

            next_update = max(
                0,
                interval - round(seconds_since_seen),
            )

            is_online = (
                seconds_since_seen < interval * 3
            )

            system = report_data.get("system", {})
            cpu = report_data.get("cpu", {})
            ram = (
                report_data
                .get("memory", {})
                .get("ram", {})
            )

            result.append(
                {
                    "hostname": host.hostname,
                    "status": (
                        "Online"
                        if is_online
                        else "Offline"
                    ),
                    "os": system.get("os", "Unknown"),
                    "cpu": cpu.get(
                        "utilization_percent"
                    ),
                    "memory": ram.get(
                        "utilization_percent"
                    ),
                    "last_seen": host.last_seen,
                    "interval": interval,
                    "next_update": next_update,
                }
            )

        return result
        
                