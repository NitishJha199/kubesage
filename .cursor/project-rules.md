# KubeSage — Project Rules

These rules govern all code and documentation changes in this repository.

---

## Project Identity

KubeSage is an **AI-powered Kubernetes troubleshooting platform** built with Python 3.12, FastAPI, and Pydantic. It follows Clean Architecture and SOLID principles.

Read before making changes:

- `docs/VISION.md` — goals and design philosophy
- `docs/ARCHITECTURE.md` — layers, pipeline, and ports
- `docs/ENGINEERING.md` — conventions, testing, and workflow

---

## Non-Negotiable Rules

### 1. Rules before AI

Deterministic rules produce findings. LLMs explain them. Never use an LLM to decide what is wrong — only to explain structured findings and suggest recommendations.

### 2. Tests for every module

Every source module must have a corresponding test module. No PR merges without tests. Domain and application layers require 90%+ coverage.

### 3. Clean Architecture boundaries

```
presentation → application → domain ← infrastructure
```

- Domain layer imports nothing from outer layers
- Infrastructure implements domain-defined ports (Protocol/ABC)
- Never import FastAPI, kubernetes, httpx, or LLM SDKs in domain/

### 4. Read-only by default

KubeSage never mutates cluster state. All collectors and API calls are read-only. No exceptions.

### 5. Evidence-backed findings

Every finding must reference the evidence that produced it. Findings without evidence references are invalid.

---

## Architecture Rules

| Layer | Directory | Responsibility |
|-------|-----------|---------------|
| Domain | `src/kubesage/domain/` | Entities, rules, correlation, scoring — pure Python |
| Application | `src/kubesage/application/` | Use cases, port interfaces |
| Infrastructure | `src/kubesage/infrastructure/` | K8s, Prometheus, Loki, OTel, LLM adapters |
| Presentation | `src/kubesage/presentation/` | FastAPI routes, middleware, serializers |

- One rule = one class in `domain/rules/`
- One collector = one class in `infrastructure/`
- One use case = one class in `application/use_cases/`
- Ports defined as `Protocol` in `application/ports/`

---

## Code Standards

### Python

- Python 3.12+, type hints on all public APIs
- Pydantic v2 models for all entities (`frozen=True` for domain entities)
- Async for all I/O; sync for rule engine evaluation
- Google-style docstrings on public classes and functions
- ruff for linting and formatting (100 char line length)

### SOLID

- **S**: One class, one responsibility
- **O**: Extend via registries (rules, collectors), not modification
- **L**: All port implementations interchangeable
- **I**: Small, focused port interfaces
- **D**: Domain defines ports; infrastructure implements

### Error Handling

- Domain exceptions in domain layer
- Wrap infrastructure errors with context at the adapter boundary
- Never catch bare `Exception`
- Graceful degradation: partial evidence is better than no diagnosis

---

## Testing Rules

- Test file mirrors source: `domain/rules/crashloop_rule.py` → `tests/unit/domain/rules/test_crashloop_rule.py`
- Unit tests: no network, use YAML fixtures from `tests/fixtures/`
- Table-driven tests with `@pytest.mark.parametrize`
- Mock LLM responses — never call real LLM APIs in tests
- Integration tests: kind cluster only, never production

---

## Kubernetes Rules

- Use the official Python kubernetes client — no subprocess calls to `kubectl`
- Always set timeouts on API calls
- Handle `ApiException` (404, 403) gracefully
- Never log or persist kubeconfig contents, tokens, or credentials
- Namespace-scoped by default; cluster-wide only when explicitly configured

---

## LLM Rules

- LLM adapter implements `LLMExplainerPort`
- Prompts built from structured `ScoredFinding` objects — never raw cluster dumps
- LLM responses validated against Pydantic schemas before use
- Fallback to template-based output when LLM is unavailable
- Provider-agnostic interface (OpenAI, Anthropic, Ollama)

---

## Documentation Rules

- Update `docs/ARCHITECTURE.md` when adding layers, ports, or changing data flow
- Update `docs/ROADMAP.md` checkboxes when completing phase items
- Do not create new markdown files unless explicitly requested
- API changes must update OpenAPI-compatible route definitions

---

## Scope Discipline

- Minimize diff size — solve the stated problem only
- No new dependencies without justification in the PR description
- No secrets, `.env` values, or kubeconfig files in commits
- No application code changes when the task is documentation-only

# Backend Development Rules

## General
- Use Python 3.11+
- Use type hints everywhere.
- Use Pydantic models for all data exchanged between modules.
- Never return raw Kubernetes client objects outside the collector layer.
- Keep modules under ~300 lines where practical.

## Collector Layer
- Only the collector talks to Kubernetes.
- Normalize Kubernetes objects into internal models.
- Do not implement diagnosis logic here.

## Diagnosis Layer
- Never call the Kubernetes API directly.
- Consume only normalized evidence.

## AI Layer
- AI explains diagnoses.
- AI does not decide diagnoses.

## Testing
- Every collector should be testable independently.
- Prefer dependency injection for Kubernetes clients.
