# KubeSage

**AI-powered Kubernetes troubleshooting platform**

KubeSage diagnoses cluster failures by collecting evidence from the Kubernetes API, Prometheus, Loki, and OpenTelemetry — correlating events, logs, metrics, and resources through deterministic rules before applying LLMs for explanation and recommendations.

Built for production. Designed for operators who need trustworthy answers under incident pressure.

---

## Why KubeSage

Kubernetes failures rarely have a single cause. A `CrashLoopBackOff` might trace back to an OOM kill, a failed liveness probe, a missing ConfigMap, or a node scheduling issue — and the evidence is scattered across Events, pod logs, metrics, and resource specs.

KubeSage unifies that evidence, applies tested diagnostic rules to produce structured findings with confidence scores, and uses LLMs only where they add value: translating technical signals into clear explanations and actionable recommendations.

## Key Features

| Capability | Description |
|------------|-------------|
| **Evidence collection** | Gathers state from the Kubernetes API, Prometheus, Loki, and OpenTelemetry |
| **Multi-signal correlation** | Links Events, Logs, Metrics, and Resources into unified incident context |
| **Deterministic diagnostics** | Rule engine runs first — predictable, testable, auditable |
| **AI-assisted explanation** | LLMs generate human-readable summaries and recommendations from structured findings |
| **Confidence scoring** | Every finding includes a scored confidence level based on evidence strength |
| **Production ready** | Timeouts, graceful degradation, RBAC-aware access, observability built in |

## Architecture at a Glance

```
 Evidence Sources          Analysis Pipeline              Output
 ─────────────────         ──────────────────             ──────
 Kubernetes API  ──┐
 Prometheus      ──┼──▶  Collect  ──▶  Correlate  ──▶  Rules  ──▶  Score  ──▶  Explain (LLM)  ──▶  Report
 Loki            ──┤
 OpenTelemetry   ──┘
```

Deterministic rules produce findings. LLMs explain them. See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full design.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.12 |
| API framework | FastAPI |
| Data validation | Pydantic v2 |
| Architecture | Clean Architecture (domain-driven layers) |
| Observability | Prometheus · Loki · OpenTelemetry |
| Testing | pytest (required for every module) |

## Documentation

| Document | Description |
|----------|-------------|
| [VISION.md](docs/VISION.md) | Problem statement, principles, and success criteria |
| [ROADMAP.md](docs/ROADMAP.md) | Development phases and milestones |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, layers, and data flow |
| [ENGINEERING.md](docs/ENGINEERING.md) | Setup, conventions, testing, and contribution guide |

## Project Status

**Early development** — documentation and architecture defined; implementation starting.

Track progress in [ROADMAP.md](docs/ROADMAP.md).

## Getting Started

> Setup instructions will be added as the application codebase lands.
> See [ENGINEERING.md](docs/ENGINEERING.md) for the planned development workflow.

```bash
git clone https://github.com/kubesage/kubesage.git
cd kubesage
```

## Contributing

Contributions are welcome. Please read [ENGINEERING.md](docs/ENGINEERING.md) before opening a pull request.

Every module requires tests. Every architectural change requires a documentation update.

## License

TBD
