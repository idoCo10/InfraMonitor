# InfraMonitor

InfraMonitor is a Linux infrastructure monitoring and inventory platform built with Python.

The InfraMonitor agent collects system, CPU, memory, storage, virtualization, and network information from Linux hosts and supports both human-readable CLI output and structured JSON.

InfraMonitor also includes a FastAPI backend and PostgreSQL database for centralized host monitoring and historical report storage. The complete stack can run through Docker Compose, with agents automatically collecting and sending monitoring reports at configurable intervals.

The project is being developed as an end-to-end DevOps platform, combining infrastructure monitoring, APIs, databases, containerization, automated testing, CI/CD, and future infrastructure-as-code and orchestration technologies.

## Current Features

### System Information

- Hostname
- Linux distribution and version
- Kernel version
- System architecture
- System uptime
- Virtualization detection
- VMware Tools version detection

### CPU

- CPU model
- Physical and logical CPU information
- VM-aware vCPU reporting
- CPU frequency
- Overall CPU utilization
- Per-core utilization
- System load averages

### Memory

- Total, used, and available memory
- Memory utilization
- Swap detection and utilization
- Physical memory hardware information when available

Some physical memory hardware information requires elevated privileges and may not be exposed by virtualized environments.

### Storage

- Physical and virtual disk discovery
- Disk size, bus, vendor, model, and serial information
- HDD / SSD / virtual disk detection
- Partition discovery
- Filesystem information
- Mount points
- LVM logical volume discovery
- Filesystem utilization

### Network

- Network interface discovery
- Interface state
- Link speed when available
- MTU
- MAC address
- IPv4 and IPv6 addresses
- RX/TX traffic statistics
- Automatic traffic unit formatting

### CLI

- Human-readable system report
- Structured JSON output
- Backend report submission
- Scheduled monitoring reports
- Standard command-line help

### Backend API

- FastAPI REST API
- Monitoring report ingestion
- Host discovery and tracking
- Latest host monitoring snapshot
- Historical reports per host
- Health and database connectivity checks

Current API endpoints include:

```text
POST /api/v1/reports
GET  /api/v1/reports
GET  /api/v1/hosts
GET  /api/v1/hosts/{hostname}
GET  /api/v1/hosts/{hostname}/reports
GET  /health
```

### Database

- PostgreSQL persistence
- Host inventory
- Historical monitoring reports
- Host-to-report relationships
- SQLAlchemy models
- Alembic database migrations
- Automatic schema migration during backend container startup

### Containerization

- Docker image support
- Host-aware monitoring from inside the agent container
- Read-only host filesystem access
- Host network monitoring
- Host disk, filesystem, and LVM monitoring
- Containerized FastAPI backend
- Containerized PostgreSQL
- Docker Compose deployment
- Service health checks and startup dependencies
- Automatic agent restart
- Containerized agent reports host information rather than container information

## Requirements

### Native Installation

- Linux
- Python 3.11+
- `pip`
- `venv`

### Container Deployment

- Linux
- Docker
- Docker Compose v2

InfraMonitor currently targets Linux systems.

## Installation

Clone the repository:

```bash
git clone https://github.com/idoCo10/InfraMonitor.git
cd InfraMonitor
```

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install InfraMonitor:

```bash
python -m pip install -e .
```

For backend and development dependencies:

```bash
python -m pip install -e ".[backend,dev]"
```

InfraMonitor is now available as a CLI command inside the virtual environment.

## Docker Deployment

InfraMonitor can deploy the monitoring agent, FastAPI backend, and PostgreSQL database through Docker Compose.

On Ubuntu, install Docker and Docker Compose v2 if they are not already available:

```bash
sudo apt update
sudo apt install docker.io docker-compose-v2
```

Ensure your user has permission to access Docker:

```bash
sudo usermod -aG docker $USER
```

Log out and back in for the group membership change to take effect.

Build and start the complete InfraMonitor stack:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

The Compose stack contains:

```text
InfraMonitor Agent
        │
        │ monitoring reports
        ▼
FastAPI Backend
        │
        ▼
PostgreSQL
```

PostgreSQL is health-checked before the backend starts. The backend automatically applies Alembic migrations before starting FastAPI, and the monitoring agent waits for the backend to become healthy before beginning report submission.

The agent uses host-aware mounts and host networking to collect information about the underlying Linux host rather than the container environment.

The container intentionally avoids privileged mode and unrestricted block-device access. Some low-level hardware metadata may therefore differ from native execution.

## Usage

Display the system report:

```bash
inframonitor
```

Display structured JSON:

```bash
inframonitor --json
```

Send a report to the backend:

```bash
inframonitor --send http://127.0.0.1:8000
```

Send reports continuously:

```bash
inframonitor \
  --send http://127.0.0.1:8000 \
  --interval 60
```

The backend URL and reporting interval can also be configured using environment variables:

```bash
INFRAMONITOR_BACKEND_URL=http://127.0.0.1:8000
INFRAMONITOR_INTERVAL=60
inframonitor
```

Display CLI help:

```bash
inframonitor --help
```

## Example Agent Output

```text
=== System Information ===
Hostname:                 localhost
OS:                       Ubuntu 24.04.4 LTS
Kernel:                   6.8.0-137-generic
Architecture:             x86_64
Uptime:                   14:56:10
Virtualization:           VMware (Tools version: 13.0.0.0 [build-24696409])

=== CPU Information ===
Model:                 Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz
vCPUs:                 4
Frequency:             2592.01 MHz
CPU Utilization:       1.5%
Per-Core Utilization:
  Core 0: 2.0%
  Core 1: 2.0%
  Core 2: 1.0%
  Core 3: 1.0%
Load Average:          1m: 0.00, 5m: 0.00, 15m: 0.00

=== Memory Information ===
Total:            7.71 GB
Used:             1.08 GB
Available:        6.63 GB
Utilization:      13.9%
Swap:             None

=== Disk Information ===
Total Disks: 1

Disk: sda
  Size:        30G
  Type:        disk
  Bus:         scsi
  Media Type:  Virtual Disk
  Vendor:      VMware
  Model:       VMware Virtual S
  Partitions:  3

  1. sda1
     Size:        1M
     Type:        part
     Mountpoints: None

  2. sda2
     Size:        2G
     Type:        part
     Filesystem:  ext4
     Mountpoints: /boot
     Total:       1.90 GB
     Used:        0.20 GB
     Free:        1.59 GB
     Utilization: 10.9%

  3. sda3
     Size:        28G
     Type:        part
     Filesystem:  LVM2_member
     Mountpoints: None

     Logical Volume: ubuntu--vg-ubuntu--lv
       Size:        14G
       Type:        lvm
       Filesystem:  ext4
       Mountpoints: /
       Total:       13.67 GB
       Used:        5.41 GB
       Free:        7.55 GB
       Utilization: 41.7%

=== Network Information ===

Interface: ens33
  Status:       UP
  Speed:        1000 Mbps
  MTU:          1500
  MAC:          00:0c:29:0a:d0:bd
  IPv4:         192.168.1.24/255.255.255.0
  IPv6:         fe80::20c:29ff:fe0a:d0bd
  Usage:        Total: 538.2 MB (RX: 506.5 MB, TX: 31.7 MB)
```

## Backend API

Check backend health:

```bash
curl http://127.0.0.1:8000/health
```

Example:

```json
{
  "status": "ok",
  "database": "connected"
}
```

List monitored hosts:

```bash
curl http://127.0.0.1:8000/api/v1/hosts
```

Get a host and its latest monitoring report:

```bash
curl http://127.0.0.1:8000/api/v1/hosts/devops24
```

Get historical reports:

```bash
curl http://127.0.0.1:8000/api/v1/hosts/devops24/reports
```

## Development

Install InfraMonitor with backend and development dependencies:

```bash
python -m pip install -e ".[backend,dev]"
```

Run the test suite:

```bash
python -m pytest
```

Run static analysis and linting:

```bash
ruff check .
```

The test suite covers:

- System collection
- CPU collection
- Memory collection
- Disk collection
- Network collection
- Main data collection
- CLI functionality
- Scheduled report submission
- Backend API
- PostgreSQL persistence
- Host management

## Database Migrations

InfraMonitor uses Alembic to manage PostgreSQL schema changes.

Check the current migration:

```bash
alembic current
```

View migration heads:

```bash
alembic heads
```

Apply migrations:

```bash
alembic upgrade head
```

When running through Docker Compose, migrations are automatically applied before the FastAPI backend starts.

## Continuous Integration

GitHub Actions automatically validates the project on:

- Pull requests targeting `main`
- Pushes to `main`

The CI pipeline:

1. Checks out the repository
2. Sets up Python 3.12
3. Starts PostgreSQL
4. Installs InfraMonitor with backend and development dependencies
5. Applies Alembic migrations
6. Runs Ruff
7. Runs the pytest test suite
8. Builds the Docker image

Workflow configuration:

```text
.github/workflows/ci.yml
```

## Project Structure

```text
InfraMonitor/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── agent/
│   └── inframonitor_agent/
│       ├── collectors/
│       │   ├── cpu.py
│       │   ├── disk.py
│       │   ├── memory.py
│       │   ├── network.py
│       │   └── system.py
│       ├── __init__.py
│       ├── client.py
│       ├── host.py
│       └── main.py
│
├── backend/
│   ├── inframonitor_api/
│   │   ├── database.py
│   │   ├── main.py
│   │   └── models.py
│   └── Dockerfile
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── conftest.py
│   ├── test_backend.py
│   ├── test_cpu.py
│   ├── test_disk.py
│   ├── test_main.py
│   ├── test_memory.py
│   ├── test_network.py
│   └── test_system.py
│
├── alembic.ini
├── compose.yaml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Architecture

InfraMonitor separates host monitoring from centralized storage and API functionality.

```text
                    Linux Host
                        │
                        ▼
                InfraMonitor Agent
                        │
              Collect system metrics
                        │
                        ▼
                 Monitoring Report
                        │
                        │ HTTP
                        ▼
                 FastAPI Backend
                        │
                        ▼
                    PostgreSQL
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
         Host Inventory      Report History
              │                   │
              └─────────┬─────────┘
                        ▼
                 REST API Layer
                        │
                        ▼
               Future Dashboard
```

The agent can run natively or inside a host-aware Docker container.

The backend is responsible for receiving reports, tracking monitored hosts, storing historical snapshots, and exposing monitoring information through the REST API.

## Docker Architecture

```text
Docker Compose

┌─────────────────────────┐
│ InfraMonitor Agent      │
│                        │
│ CPU / RAM / Disk / Net │
└────────────┬────────────┘
             │
             │ every 60 seconds
             ▼
┌─────────────────────────┐
│ FastAPI Backend         │
│                        │
│ REST API               │
│ Alembic migrations     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ PostgreSQL              │
│                        │
│ hosts                  │
│ reports                │
└─────────────────────────┘
```

A fresh deployment can initialize the complete stack using:

```bash
docker compose up -d --build
```

## Roadmap

### Phase 1 — Linux Agent

- [x] System information collection
- [x] Virtualization detection
- [x] CPU inventory and utilization
- [x] Memory utilization
- [x] Disk and partition inventory
- [x] LVM discovery
- [x] Disk utilization
- [x] Network interface inventory
- [x] Network traffic statistics
- [x] Automated tests
- [x] Installable CLI
- [x] Structured JSON output

### Phase 2 — Backend & Containers

- [x] Dockerize InfraMonitor agent
- [x] Host-aware container monitoring
- [x] FastAPI backend
- [x] Agent-to-backend communication
- [x] Scheduled agent reporting
- [x] PostgreSQL persistence
- [x] Host inventory and report history
- [x] Alembic database migrations
- [x] Containerized FastAPI backend
- [x] Multi-container Docker Compose environment
- [x] Automatic database migrations
- [x] Container health checks and startup dependencies
- [ ] Web monitoring dashboard

### Phase 3 — CI/CD

- [x] GitHub Actions CI pipeline
- [x] Automated linting
- [x] Automated test execution
- [x] PostgreSQL integration testing
- [x] Database migration testing
- [x] Docker image build validation
- [ ] Container registry
- [ ] Automated deployment workflow

### Phase 4 — Infrastructure as Code

- [ ] Terraform
- [ ] AWS infrastructure
- [ ] Automated environment provisioning

### Phase 5 — Orchestration & Observability

- [ ] Kubernetes deployment
- [ ] Helm charts
- [ ] Prometheus integration
- [ ] Grafana dashboards
- [ ] Centralized logging

### Phase 6 — Security

- [ ] Host security checks
- [ ] Firewall status
- [ ] Listening port inventory
- [ ] SSH configuration auditing
- [ ] User and authentication auditing
- [ ] DevSecOps checks integrated into CI/CD

## Technology Stack

**Currently implemented**

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- psutil
- pytest
- Ruff
- Git
- GitHub Actions
- Docker
- Docker Compose
- Linux system utilities

**Planned**

- Web dashboard
- Terraform
- AWS
- Kubernetes
- Helm
- Prometheus
- Grafana

## License

MIT