# Roadmap

Development follows a phased approach: establish a deterministic diagnostic core first, then layer on observability integrations, AI explanation, and production hardening.

---

## Phase 0 — Foundation

**Goal:** Project structure, tooling, and architectural skeleton.

- [x] Project documentation (VISION, ROADMAP, ARCHITECTURE, ENGINEERING)
- [ ] Python 3.12 project scaffold (pyproject.toml, dependency management)
- [ ] Clean architecture directory layout
- [ ] FastAPI application skeleton with health endpoints
- [ ] Pydantic domain models for core entities (Finding, Evidence, ConfidenceScore)
- [ ] CI pipeline: lint (ruff), type check (mypy), test (pytest), coverage gate
- [ ] Pre-commit hooks

**Exit criteria:** `pytest` runs green on scaffold; CI passes on every PR.

---

## Phase 1 — Evidence Collection

**Goal:** Read-only data gathering from Kubernetes and observability backends.

- [ ] Kubernetes API collector (pods, deployments, events, nodes, services)
- [ ] Prometheus query client (PromQL for resource and probe metrics)
- [ ] Loki query client (LogQL for pod and container logs)
- [ ] OpenTelemetry trace/metric correlation hooks
- [ ] Evidence normalization into domain models
- [ ] Collector integration tests against kind cluster + mock observability backends

**Exit criteria:** Single API call returns a unified evidence bundle for a target workload.

---

## Phase 2 — Deterministic Diagnostics

**Goal:** Rule engine that produces structured, scored findings without LLM involvement.

- [ ] Rule engine framework (register, evaluate, compose rules)
- [ ] Correlation engine (link Events ↔ Logs ↔ Metrics ↔ Resources)
- [ ] Confidence scoring model
- [ ] Initial rule set:
  - CrashLoopBackOff (exit codes, OOMKilled, probe failures)
  - Pod Pending (scheduling constraints, resource quotas, taints)
  - ImagePullBackOff / ErrImagePull
  - Node NotReady / pressure conditions
  - Service endpoint mismatches
  - ConfigMap / Secret mount failures
- [ ] Fixture library (YAML snapshots of common failure scenarios)
- [ ] 100% test coverage on rules and correlation logic

**Exit criteria:** Rule engine diagnoses top-10 failure modes from fixtures with deterministic output and confidence scores.

---

## Phase 3 — AI Explanation Layer

**Goal:** LLM integration strictly limited to explanation and recommendations.

- [ ] LLM adapter interface (provider-agnostic: OpenAI, Anthropic, local models)
- [ ] Prompt templates that consume structured findings + evidence (never raw dumps)
- [ ] Explanation generator: finding → human-readable summary
- [ ] Recommendation generator: finding → actionable next steps
- [ ] Guardrails: LLM output validated against Pydantic schemas
- [ ] Fallback: structured JSON output when LLM is unavailable
- [ ] Tests with mocked LLM responses

**Exit criteria:** Given a structured finding, the system produces a validated explanation and recommendation. LLM failure degrades gracefully to structured output.

---

## Phase 4 — API and Integration

**Goal:** Production FastAPI service exposing diagnostic capabilities.

- [ ] `POST /diagnose` — run full diagnostic pipeline for a workload
- [ ] `GET /findings/{id}` — retrieve a previous diagnostic result
- [ ] `GET /health`, `GET /ready` — liveness and readiness probes
- [ ] OpenAPI documentation (auto-generated)
- [ ] Request validation via Pydantic
- [ ] Async evidence collection with concurrency limits
- [ ] Structured logging (JSON) with correlation IDs
- [ ] OpenTelemetry instrumentation (traces, metrics, logs)

**Exit criteria:** Service deployable to Kubernetes; passes load test against kind cluster with 100 concurrent diagnoses.

---

## Phase 5 — Production Hardening

**Goal:** Operability, security, and scale for real-world deployment.

- [ ] RBAC documentation and minimal ClusterRole manifest
- [ ] Configuration via environment variables and ConfigMap
- [ ] Rate limiting and timeout policies per upstream (K8s API, Prometheus, Loki)
- [ ] Circuit breakers for degraded upstream availability
- [ ] Helm chart for Kubernetes deployment
- [ ] Grafana dashboard for KubeSage operational metrics
- [ ] Security audit: no credential logging, no persistent cluster data by default
- [ ] Performance benchmarks (latency, memory) documented

**Exit criteria:** Helm-deployable; operational runbook complete; security review passed.

---

## Phase 6 — Ecosystem

**Goal:** Extend reach through integrations and extensibility.

- [ ] Custom rule plugin API
- [ ] Slack / Microsoft Teams notification adapter
- [ ] GitHub Action for pre-deploy cluster health checks
- [ ] CLI client (`kubesage diagnose`)
- [ ] Multi-cluster support
- [ ] Historical trend analysis (optional persistent store)

---

## Milestones

| Milestone | Phase | Definition of Done |
|-----------|-------|-------------------|
| **M0** | 0 | Docs complete, CI green, project scaffold merged |
| **M1** | 1–2 | Evidence collection + rule engine diagnose CrashLoopBackOff from fixtures |
| **M2** | 2–3 | Top-10 failure modes diagnosed with confidence scores and LLM explanations |
| **M3** | 4 | FastAPI service deployed to kind; `/diagnose` endpoint functional |
| **M4** | 5 | Helm chart published; production runbook available |
| **M5** | 6 | CLI and at least one integration adapter shipped |

Dates will be set as phases complete. Track open items via GitHub Issues and Project board.
