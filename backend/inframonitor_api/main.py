from typing import Any

from fastapi import FastAPI

app = FastAPI(
    title="InfraMonitor API",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/reports")
def receive_report(report: dict[str, Any]):
    #print(report) # debug

    return {
        "status": "received",
        "hostname": report.get("system", {}).get("hostname"),
    }