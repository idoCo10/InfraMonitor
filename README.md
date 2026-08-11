# InfraGuard

Infrastructure inventory, monitoring, and security auditing platform designed for Linux environments.

InfraGuard collects hardware, operating system, network, performance, and security information from managed hosts through lightweight agents and presents the data through a centralized web dashboard.

The project aims to provide a unified view of infrastructure assets, resource utilization, network activity, and basic security posture while serving as a practical DevOps and DevSecOps learning platform.

---

## Features

### Asset Inventory

* Hostname and system identification
* Operating system and kernel information
* Physical or virtual machine detection
* CPU model and core information
* Memory configuration and utilization
* Storage devices and partition details
* Network interface inventory

### Monitoring

* CPU utilization
* Memory utilization
* Disk utilization
* Network traffic statistics
* Historical metric collection

### Security Auditing

* Firewall status verification
* Open port discovery
* SSH configuration auditing
* User and group inventory
* Login activity tracking
* Security posture assessment

### Dashboard

* Centralized asset inventory
* Infrastructure overview
* Performance monitoring
* Security visibility
* Historical data visualization

---

## Architecture

```text
+-------------------+
|   InfraGuard      |
|      Agent        |
+---------+---------+
          |
          | HTTPS / REST API
          |
+---------v---------+
|   InfraGuard      |
|      Backend      |
+---------+---------+
          |
          |
+---------v---------+
|    PostgreSQL     |
+---------+---------+
          |
          |
+---------v---------+
|   Web Dashboard   |
+-------------------+
```

---

## Technology Stack

### Backend

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy

### Agent

* Python
* psutil
* Linux system utilities

### DevOps

* Docker
* Docker Compose
* GitHub Actions
* Kubernetes
* Helm
* Terraform

### Monitoring & Observability

* Prometheus
* Grafana

---

## Project Goals

* Build a centralized infrastructure inventory platform
* Monitor Linux hosts in real time
* Improve infrastructure visibility
* Implement security auditing capabilities
* Practice modern DevOps workflows and tooling
* Demonstrate end-to-end software delivery using CI/CD pipelines

---

## Development Roadmap

### Phase 1 – Asset Inventory

* [ ] Host information collection
* [ ] Operating system detection
* [ ] CPU information collection
* [ ] Memory information collection
* [ ] Storage inventory
* [ ] Network adapter inventory

### Phase 2 – Monitoring

* [ ] CPU metrics
* [ ] Memory metrics
* [ ] Disk metrics
* [ ] Network metrics
* [ ] Historical data storage

### Phase 3 – Security

* [ ] Firewall auditing
* [ ] Open port detection
* [ ] User inventory
* [ ] Login auditing
* [ ] Security scoring

### Phase 4 – DevOps

* [ ] Docker deployment
* [ ] CI/CD pipeline
* [ ] Kubernetes deployment
* [ ] Infrastructure as Code

---

## Current Status

Project initialization and architecture planning.

---

## License

MIT License
