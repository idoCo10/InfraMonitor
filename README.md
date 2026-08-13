# InfraMonitor

InfraMonitor is a Linux infrastructure monitoring and inventory project built with Python.

The agent collects system, CPU, memory, storage, virtualization, and network information from Linux hosts. The project is being developed as an end-to-end DevOps platform, with planned containerization, CI/CD, centralized monitoring, infrastructure as code, and Kubernetes deployment.

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
- Physical/logical CPU information
- VM-aware vCPU reporting
- CPU frequency
- Overall CPU utilization
- Per-core utilization
- System load averages

### Memory

- Total, used, and available memory
- Memory utilization
- Swap detection and utilization
- Memory hardware information when available

Some hardware information requires elevated privileges and may not be exposed by virtualized environments.

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
- Link speed
- MTU
- MAC address
- IPv4 and IPv6 addresses
- RX/TX traffic statistics
- Automatic traffic unit formatting

## Requirements

- Linux
- Python 3.11+
- `pip`
- `venv`

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

Install InfraMonitor in editable mode:

```bash
python -m pip install -e .
```

InfraMonitor is now available as a CLI command inside the virtual environment.

## Usage

Run:

```bash
inframonitor
```

Example:

```text
=== System Information ===
Hostname:                 devops24
OS:                       Ubuntu 24.04.4 LTS
Kernel:                   6.8.0-137-generic
Architecture:             x86_64
Virtualization:           VMware

=== CPU Information ===
Model:                 Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz
vCPUs:                 4
CPU Utilization:       1.8%

=== Memory Information ===
Total:        7.71 GB
Used:         1.05 GB
Available:    6.66 GB
Utilization:  13.6%

=== Disk Information ===
Total Disks: 1

=== Network Information ===
Interface: ens33
  Status:       UP
  Speed:        1000 Mbps
```

## Development Setup

Install the project with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the test suite:

```bash
python -m pytest
```

The project currently includes tests for:

- System collection
- CPU collection
- Memory collection
- Disk collection
- Network collection

## Project Structure

```text
InfraMonitor/
├── agent/
│   └── inframonitor_agent/
│       ├── collectors/
│       │   ├── cpu.py
│       │   ├── disk.py
│       │   ├── memory.py
│       │   ├── network.py
│       │   └── system.py
│       └── main.py
├── tests/
├── pyproject.toml
└── README.md
```

## Architecture

The current implementation consists of a standalone Linux agent.

The planned architecture is:

```text
Linux Hosts
    │
    │ InfraMonitor Agent
    ▼
Backend API
    │
    ▼
PostgreSQL
    │
    ├── Monitoring / Metrics
    │
    └── Web Dashboard
```

The agent is being developed first so that infrastructure collection remains independent from the backend and deployment platform.

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
- [ ] Structured JSON output

### Phase 2 — Application & Containers

- [ ] FastAPI backend
- [ ] Agent-to-backend communication
- [ ] PostgreSQL persistence
- [ ] Dockerize application components
- [ ] Docker Compose development environment

### Phase 3 — CI/CD

- [ ] GitHub Actions test pipeline
- [ ] Automated Docker builds
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
- psutil
- Linux
- pytest
- Git

**Planned**

- FastAPI
- PostgreSQL
- Docker / Docker Compose
- GitHub Actions
- Terraform
- AWS
- Kubernetes
- Helm
- Prometheus
- Grafana

## License

MIT
