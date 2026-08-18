import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def send_report(report, backend_url):
    """Send an InfraMonitor report to the backend API."""

    url = f"{backend_url.rstrip('/')}/api/v1/reports"

    request = Request(
        url,
        data=json.dumps(report).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        raise RuntimeError(
            f"Backend returned HTTP {error.code}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Could not connect to backend: {error.reason}"
        ) from error
