# InfraMonitor

InfraMonitor is a Linux infrastructure monitoring and inventory agent built with Python.

The agent collects system, CPU, memory, storage, virtualization, and network information from Linux hosts and exposes the collected data through both human-readable CLI output and structured JSON.

The project is being developed as an end-to-end DevOps platform, with automated testing and CI already implemented and containerization, centralized monitoring, infrastructure as code, and Kubernetes deployment planned.

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
- Standard command-line help

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

Install InfraMonitor:

```bash
python -m pip install -e .
```

InfraMonitor is now available as a CLI command inside the virtual environment.

## Usage

Display the system report:

```bash
inframonitor
```

Display structured JSON:

```bash
inframonitor --json
```

Display CLI help:

```bash
inframonitor --help
```

Example output:

```text
=== System Information ===
Hostname:                 localhost
OS:                       Ubuntu 24.04.4 LTS
Kernel:                   6.8.0-137-generic
Architecture:             x86_64
Uptime:                   9:58:59
Virtualization:           VMware (Tools version: 13.0.0.0 [build-24696409])

=== CPU Information ===
Model:                 Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz
vCPUs:                 4
Frequency:             2592.01 MHz
CPU Utilization:       3.5%
Per-Core Utilization:
  Core 0: 4.0%
  Core 1: 3.0%
  Core 2: 4.0%
  Core 3: 3.0%
Load Average:          1m: 0.02, 5m: 0.01, 15m: 0.00

=== Memory Information ===
Total:            7.71 GB
Used:             1.11 GB
Available:        6.60 GB
Utilization:      14.4%
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

=== Network Information ===

Interface: ens33
  Status:       UP
  Speed:        1000 Mbps
  MTU:          1500
  MAC:          00:0c:29:0a:d0:bd
  IPv4:         192.168.1.24/255.255.255.0
  IPv6:         fe80::20c:29ff:fe0a:d0bd
  Usage:        Total: 504.5 MB (RX: 483.2 MB, TX: 21.2 MB)
```

## Development

Install InfraMonitor with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the test suite:

```bash
python -m pytest
```

Run static analysis and linting:

```bash
ruff check .
```

The current test suite covers:

- System collection
- CPU collection
- Memory collection
- Disk collection
- Network collection
- Main data collection and CLI functionality

## Continuous Integration

GitHub Actions automatically validates the project on:

- Pull requests targeting `main`
- Pushes to `main`

The CI pipeline:

1. Checks out the repository
2. Sets up Python 3.12
3. Installs InfraMonitor with development dependencies
4. Runs Ruff
5. Runs the pytest test suite

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
├── agent/
│   └── inframonitor_agent/
│       ├── collectors/
│       │   ├── cpu.py
│       │   ├── disk.py
│       │   ├── memory.py
│       │   ├── network.py
│       │   └── system.py
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── test_cpu.py
│   ├── test_disk.py
│   ├── test_main.py
│   ├── test_memory.py
│   ├── test_network.py
│   └── test_system.py
├── pyproject.toml
└── README.md
```

## Architecture

The current implementation consists of a standalone Linux agent.

```text
Linux Host
    │
    ▼
InfraMonitor Agent
    │
    ├── System Collector
    ├── CPU Collector
    ├── Memory Collector
    ├── Disk Collector
    └── Network Collector
            │
            ▼
      Structured Data
        │         │
        ▼         ▼
    CLI Output   JSON
```

The planned centralized architecture is:

```text
Linux Hosts
    │
    │ InfraMonitor Agents
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

The agent is being developed independently from the backend so that host data collection remains separate from storage, visualization, and deployment components.

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

### Phase 2 — Application & Containers

- [ ] FastAPI backend
- [ ] Agent-to-backend communication
- [ ] PostgreSQL persistence
- [ ] Dockerize application components
- [ ] Docker Compose development environment

### Phase 3 — CI/CD

- [x] GitHub Actions CI pipeline
- [x] Automated linting
- [x] Automated test execution
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
- pytest
- Ruff
- Git
- GitHub Actions
- Linux system utilities

**Planned**

- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- Terraform
- AWS
- Kubernetes
- Helm
- Prometheus
- Grafana

## License

MIT
