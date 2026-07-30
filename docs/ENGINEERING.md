# Engineering Guide

Standards and workflows for contributing to KubeSage.

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12+ | Runtime |
| uv or pip | latest | Dependency management |
| Docker | latest | kind cluster for integration tests |
| kind | latest | Local Kubernetes cluster |
| kubectl | latest | Cluster interaction |

---

## Tech Stack

| Component | Choice | Notes |
|-----------|--------|-------|
| Language | Python 3.12 | Type hints required on all public APIs |
| Web framework | FastAPI | Async endpoints, auto OpenAPI |
| Validation | Pydantic v2 | All domain entities and API schemas |
| K8s client | kubernetes (official Python client) | Async where available |
| HTTP client | httpx | Async calls to Prometheus, Loki |
| OTel | opentelemetry-sdk | Traces, metrics, logs |
| Testing | pytest + pytest-asyncio | Required for every module |
| Linting | ruff | Formatting + linting |
| Type checking | mypy (strict) | All src/ code |
| Coverage | pytest-cov | Minimum 90% on domain and application layers |

---

## Repository Layout

```
kubesage/
├── src/kubesage/
│   ├── domain/              # Pure business logic — no I/O imports
│   ├── application/         # Use cases and port interfaces
│   ├── infrastructure/      # External system adapters
│   └── presentation/        # FastAPI routes and middleware
├── tests/
│   ├── unit/                # Fast, no network
│   ├── integration/         # kind cluster + mock backends
│   └── fixtures/            # YAML evidence and resource snapshots
├── docs/                    # Project documentation
├── .cursor/                 # Cursor IDE rules
├── pyproject.toml
├── README.md
└── .gitignore
```

### Layer Import Rules

Enforced by convention and linting:

| Layer | May import from | Must NOT import from |
|-------|----------------|---------------------|
| `domain/` | stdlib, pydantic | application, infrastructure, presentation |
| `application/` | domain | infrastructure, presentation |
| `infrastructure/` | domain, application (ports only) | presentation |
| `presentation/` | application, domain (entities for serialization) | infrastructure (directly) |

---

## SOLID Principles

KubeSage applies SOLID throughout:

| Principle | Application |
|-----------|------------|
| **S** — Single Responsibility | One rule = one class. One collector = one source. |
| **O** — Open/Closed | Rules registered via registry; new rules added without modifying engine. |
| **L** — Liskov Substitution | All collectors implement `EvidenceCollectorPort` interchangeably. |
| **I** — Interface Segregation | Separate ports for collection, explanation, and recommendation. |
| **D** — Dependency Inversion | Domain defines ports; infrastructure implements them. |

---

## Development Setup

> Commands below reflect the planned project scaffold. Update as implementation lands.

```bash
git clone https://github.com/kubesage/kubesage.git
cd kubesage

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check src/ tests/
ruff format --check src/ tests/

# Run type checker
mypy src/
```

### Local Kubernetes Cluster

```bash
kind create cluster --name kubesage-dev
kubectl cluster-info --context kind-kubesage-dev
```

Apply fixtures to simulate failures:

```bash
kubectl apply -f tests/fixtures/scenarios/crashloop/
```

---

## Testing Requirements

**Every module must have tests.** No exceptions.

### Test Categories

| Category | Location | Scope | Network |
|----------|----------|-------|---------|
| Unit | `tests/unit/` | Domain rules, correlation, scoring, Pydantic models | No |
| Integration | `tests/integration/` | Collectors against kind; API endpoints | kind cluster |
| Fixtures | `tests/fixtures/` | YAML snapshots of K8s resources, events, metrics, logs | N/A |

### Unit Test Standards

- Table-driven tests with `pytest.mark.parametrize`
- One test file per source module: `test_<module_name>.py`
- Fixtures in `tests/fixtures/` — never fetch live cluster data in unit tests
- Mock all I/O at infrastructure boundaries

Example structure:

```python
@pytest.mark.parametrize("fixture,expected_finding", [
    ("crashloop_oom.yaml", "OOMKilledRule"),
    ("crashloop_probe.yaml", "ProbeFailureRule"),
])
def test_crashloop_rules(fixture, expected_finding, load_fixture):
    evidence = load_fixture(fixture)
    findings = rule_engine.evaluate(evidence)
    assert any(f.rule_name == expected_finding for f in findings)
```

### Coverage Requirements

| Layer | Minimum Coverage |
|-------|-----------------|
| `domain/` | 95% |
| `application/` | 90% |
| `infrastructure/` | 80% |
| `presentation/` | 80% |

CI enforces these gates. PRs that reduce coverage below thresholds will fail.

### Integration Test Standards

- Run against a kind cluster created in CI
- Mock Prometheus, Loki, and LLM endpoints (httpx mock or test containers)
- Clean up resources after each test
- Timeout: 60 seconds per integration test

---

## Coding Conventions

### Python Style

- PEP 8 enforced by ruff
- Type hints on all function signatures and class attributes
- Docstrings on public classes and functions (Google style)
- Max line length: 100
- Prefer `pathlib` over `os.path`
- Use `async/await` for all I/O operations

### Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Modules | snake_case | `crashloop_rule.py` |
| Classes | PascalCase | `CrashLoopBackOffRule` |
| Functions | snake_case | `evaluate_findings` |
| Constants | UPPER_SNAKE | `DEFAULT_TIMEOUT_SECONDS` |
| Test files | `test_<module>.py` | `test_crashloop_rule.py` |

### Error Handling

- Domain layer raises domain exceptions (`FindingError`, `RuleEvaluationError`)
- Application layer catches domain exceptions and maps to application errors
- Presentation layer maps application errors to HTTP status codes
- Never catch bare `Exception` — be specific
- Wrap infrastructure errors with context:

```python
raise EvidenceCollectionError(
    f"Failed to query Prometheus for pod {pod_name}: {cause}"
) from cause
```

### Pydantic Models

- All domain entities are Pydantic `BaseModel` with `model_config = ConfigDict(frozen=True)`
- Use `Field()` with descriptions for API-facing models
- Validate at boundaries — trust nothing from external sources

### Async Patterns

- All collector and LLM methods are `async`
- Use `asyncio.gather()` for concurrent evidence collection with `return_exceptions=True`
- Set per-call timeouts via `asyncio.timeout()` (Python 3.12+)
- Rule engine runs synchronously (CPU-bound, no I/O)

---

## Git Workflow

### Branching

```
main          ← stable, protected
└── feat/…    ← feature branches
└── fix/…     ← bug fixes
└── docs/…    ← documentation updates
```

### Commit Messages

Conventional Commits format:

```
<type>(<scope>): <summary>

[optional body]
```

| Type | Usage |
|------|-------|
| `feat` | New feature or rule |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Test additions or fixes |
| `refactor` | Code change without behavior change |
| `chore` | Tooling, CI, dependencies |

Examples:

```
feat(rules): add OOMKilledRule with memory metric correlation
fix(prometheus): handle empty query result gracefully
test(correlation): add temporal proximity edge case fixtures
```

### Pull Request Checklist

- [ ] Tests added/updated for every changed module
- [ ] Coverage thresholds maintained
- [ ] Type hints complete (mypy passes)
- [ ] Lint passes (ruff)
- [ ] Documentation updated if architecture or API changed
- [ ] No secrets, credentials, or kubeconfig committed

---

## CI Pipeline

Runs on every push and pull request:

```yaml
# Planned pipeline stages
lint:       ruff check + ruff format --check
typecheck:  mypy src/
test:       pytest --cov --cov-fail-under=90
integration: pytest tests/integration/ (kind cluster)
```

---

## Configuration

Environment variables (planned):

| Variable | Required | Description |
|----------|----------|-------------|
| `KUBESAGE_KUBECONFIG` | No | Path to kubeconfig (default: in-cluster or `~/.kube/config`) |
| `KUBESAGE_PROMETHEUS_URL` | No | Prometheus server URL |
| `KUBESAGE_LOKI_URL` | No | Loki server URL |
| `KUBESAGE_OTEL_ENDPOINT` | No | OpenTelemetry collector endpoint |
| `KUBESAGE_LLM_PROVIDER` | No | LLM provider (`openai`, `anthropic`, `ollama`) |
| `KUBESAGE_LLM_API_KEY` | No | API key for LLM provider |
| `KUBESAGE_LOG_LEVEL` | No | Logging level (default: `INFO`) |

Missing optional variables degrade gracefully — the system collects what it can from available sources.

---

## Observability (Dogfooding)

KubeSage instruments itself with the same stack it consumes:

- **Traces** — OpenTelemetry, exported via OTLP
- **Metrics** — Prometheus-compatible (`/metrics` endpoint)
- **Logs** — Structured JSON to stdout (Loki-ingestible)

Key operational metrics:

| Metric | Type | Description |
|--------|------|-------------|
| `kubesage_diagnosis_duration_seconds` | Histogram | End-to-end diagnosis latency |
| `kubesage_evidence_collection_errors_total` | Counter | Failed collection attempts by source |
| `kubesage_rules_evaluated_total` | Counter | Rules evaluated per diagnosis |
| `kubesage_llm_requests_total` | Counter | LLM API calls |
| `kubesage_confidence_score` | Histogram | Distribution of confidence scores |

---

## Dependency Management

- Dependencies declared in `pyproject.toml`
- Pin major versions; use compatible release for minors
- Dev dependencies in `[project.optional-dependencies.dev]`
- Review new dependencies in PRs — prefer stdlib and existing deps over new packages
- No dependencies in the domain layer

---

## Local Development Tips

1. **Start with domain** — write rules and tests before wiring collectors
2. **Use fixtures** — build a rich fixture library early; it pays off across all test layers
3. **Mock LLMs** — never call real LLM APIs in tests; use response fixtures
4. **Kind over minikube** — faster startup, easier CI replication
5. **Run mypy continuously** — catch type errors early, not in CI
