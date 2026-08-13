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
       Used:        5.37 GB
       Free:        7.59 GB
       Utilization: 41.4%


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
