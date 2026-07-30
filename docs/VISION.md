# Vision

## Problem

Kubernetes incidents are multi-dimensional. A single failing pod can surface as Events in one namespace, error logs in Loki, memory spikes in Prometheus, and scheduling constraints in node metrics — each in a different tool, with no shared context.

Operators spend critical minutes during outages manually correlating signals:

- Scanning `kubectl describe` and Events for clues
- Searching Loki for stack traces and error patterns
- Querying Prometheus for resource saturation or probe failures
- Cross-referencing resource specs against observed behavior

Existing tools report *what* is broken. They rarely explain *why*, with evidence, at the moment it matters.

## Solution

KubeSage is an AI-powered Kubernetes troubleshooting platform that:

1. **Collects evidence** from the Kubernetes API, Prometheus, Loki, and OpenTelemetry
2. **Correlates signals** across Events, Logs, Metrics, and Resources into a unified incident view
3. **Diagnoses failures** using deterministic, testable rules — not probabilistic guessing
4. **Explains findings** via LLMs that receive structured evidence, not raw cluster dumps
5. **Scores confidence** so operators know which conclusions are strong and which need verification

## Design Philosophy

### Rules before AI

Deterministic rules are the source of truth. They are:

- **Testable** — every rule has fixture-based unit tests
- **Auditable** — operators can inspect exactly what logic fired
- **Reliable** — same inputs always produce the same findings

LLMs are used exclusively for **explanation and recommendations** — translating structured findings into clear, actionable language. They never decide *what* is wrong; they explain *why the rules concluded what they did* and suggest next steps.

### Evidence over intuition

Every finding must cite the evidence that produced it: the Event, log line, metric threshold, or resource field. Findings without evidence are not findings.

### Confidence scoring

Each diagnostic conclusion carries a confidence score derived from:

- Number and quality of corroborating signals
- Specificity of the matched rule
- Absence of conflicting evidence

Operators can prioritize high-confidence findings during incidents and investigate low-confidence ones with appropriate skepticism.

### Production first

KubeSage is designed to run against real clusters under real incident conditions:

- Read-only by default
- RBAC-aware with graceful permission degradation
- Timeouts and circuit breakers on all external calls
- Observable via OpenTelemetry, with metrics exportable to Prometheus

## Principles

| # | Principle | Meaning |
|---|-----------|---------|
| 1 | **Deterministic core** | Rules engine decides; LLMs explain |
| 2 | **Evidence-backed findings** | Every conclusion links to source data |
| 3 | **Multi-signal correlation** | Events, logs, metrics, and resources analyzed together |
| 4 | **Confidence transparency** | Scored findings, never false certainty |
| 5 | **Safe by default** | Read-only analysis; no autonomous mutations |
| 6 | **Clean architecture** | Domain logic independent of frameworks and I/O |
| 7 | **Test everything** | Every module has tests; no exceptions |

## Target Users

- **SRE / Platform engineers** triaging production incidents
- **On-call responders** who need fast, evidence-backed root cause hypotheses
- **Developer teams** deploying workloads to Kubernetes without deep cluster expertise
- **Security and compliance teams** auditing cluster health and policy adherence

## Success Criteria

- Reduce mean time to understand (MTTU) for the top Kubernetes failure modes
- Produce findings that operators trust without re-verifying every signal manually
- Maintain deterministic reproducibility: same cluster state → same rule findings
- LLM explanations rated as clear and actionable by operator feedback
- Run reliably against production-scale clusters (1000+ pods) within acceptable latency

## Non-Goals

- **Autonomous remediation** — KubeSage advises; humans act
- **Replacing observability stacks** — it consumes Prometheus, Loki, and OpenTelemetry; it does not replace them
- **Infrastructure provisioning** — no Terraform, no cluster creation
- **LLM-as-judge** — models do not determine diagnostic conclusions
