# 🐍 spec-objects-safety

> Filament Module: safety ObjectTypes (hazard, failure_mode) — IEC 61508 / ISO 26262 / FMEA

---

## 🧭 What this module ships

The package root **is** the Filament module. `spec_objects_safety/manifest.yaml`
declares two object types — `hazard` (a system state that can lead to harm) and
`failure_mode` (the manner in which a component fails) — with their body
contracts, their authoring skeletons, the domain lexicon, and the
`traceability` model that reports a hazard nothing mitigates.

Since 0.3.0 it is a **semantic module** (quoin FR-070): the archetypes are
authored in `typespec/main.tsp` against `@agent-ix/semantic-core`, emitted to
JSON Schema 2020-12 under `spec_objects_safety/schemas/`, and referenced from
the manifest by path and digest.

The rule those schemas exist to enforce: every scored axis — severity,
likelihood, ISO 26262 exposure and controllability, FMEA detection — admits
either its own ordinal scale **or** one of `unknown`, `not_assessed`,
`not_applicable`. Those three share no member with any scale, so an axis nobody
looked at can never be read, sorted or scored as a safe one. Nothing here
defaults a safety judgement, and `status: accepted` requires a `provenance`
naming who accepted the risk and when.

### Working on the schemas

```bash
make schemas        # re-emit spec_objects_safety/schemas/ from typespec/main.tsp
make schemas-check  # fail on schema or digest drift (also run by `make lint`)
make dev-quire      # install the Quire wheel the semantic tests need
```

`make schemas` needs `npm ci` first and a user-level npm config that routes
`@agent-ix` to npm.ix; the repository carries no `.npmrc`. A wrong schema is
fixed in `typespec/main.tsp` and regenerated — never hand-edited.

`make dev-quire` exists because the Quire build exposing `extract_semantic` is
on no index this repository may commit a dependency against
(`agent-ix/quire-rs#392`). Without it the semantic tests **fail**; they never
skip, because a skipped row is not coverage.

---

## 📐 Project Structure and Development Philosophy

- **Library Name:** `spec_objects_safety`
- **Layout:** Flat project layout (package at root, no `src/`)
- **Language:** Python 3.13+
- **Dependency Management:** [Poetry](https://python-poetry.org/)
- **Build and CI:** GitHub Actions
- **Publishing:** Google Artifact Registry (PyPI-compatible)

---

## 🛠 Prerequisites

- **Python 3.13+** installed on your system
- **Poetry 2.x** installed (`pip install poetry` or [official installer](https://python-poetry.org/docs/#installation))
- **devpi-client** (optional, for local publishing): `pip install devpi-client`

---

## 🚀 Quick Start

```bash
# Install dependencies and create venv
make install

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Build distribution
make build
```

---

## 📦 Build Process

- **Local Development**:
  - `make install` - Install dependencies in Poetry venv
  - `make test` - Run tests
  - `make format` - Auto-format code (Black + Ruff)
  - `make lint` - Run linting checks
- **Artifact Building**:
  - `make build` - Build wheel and sdist under `dist/`
- **Artifact Upload**:
  - Artifacts uploaded via `twine upload` in CI

---

## 🚀 Continuous Integration (CI)

- **GitHub Actions Workflow**:
  - Triggers: `push`, `pull_request`, `tag v*.*.*`
  - Runs tests and lint checks
  - Builds artifacts with `poetry build`
  - Publishes to Google Artifact Registry using `twine upload -r internal-pypi`

---

## 🔑 Required GitHub Secrets

| Secret Name | Purpose |
|:------------|:--------|
| `GCP_SERVICE_ACCOUNT_KEY` | Raw JSON of GCP Service Account Key |

| Variable Name | Purpose |
|:------------|:--------|
| `GCP_REGION` | GCP Region for Artifact Registry (e.g., `us-west1`) |
| `GCP_PROJECT_NAME` | GCP Project ID (e.g., `agent-ix`) |
| `GCP_PYPI` | Artifact Registry repository name (e.g., `internal-pypi`) |

---

## 🐳 Makefile Targets

| Target | Description |
|:-------|:------------|
| `install` | Install dependencies in Poetry venv |
| `build` | Build wheel and sdist artifacts |
| `test` | Run tests |
| `lint` | Run linting (Ruff + Black check + schema drift gate) |
| `schemas` | Re-emit `spec_objects_safety/schemas/` from `typespec/main.tsp` |
| `schemas-check` | Fail on schema or manifest-digest drift |
| `dev-quire` | Install the Quire wheel the semantic tests need |
| `format` | Auto-format code (Black + Ruff --fix) |
| `shell` | Open Poetry shell |
| `clean` | Remove all build artifacts |
| `version` | Show project version |
| `info` | Show Git and version info |
| `update-lock` | Update poetry.lock |
| `update-packages` | Update all dependencies |
| `add-package p=<name>` | Add a production dependency |
| `add-dev-package p=<name>` | Add a dev dependency |
| `local-publish` | Build and publish to local PyPI |

---

## 🏠 Local Development with Local PyPI

For local development and testing, you can publish packages to the local PyPI proxy.

### Prerequisites

1. **Local Kubernetes cluster** running with PyPI proxy:
   ```bash
   # In the local repo
   make up
   make pypi-up
   ```

2. **devpi-client** installed locally:
   ```bash
   pip install devpi-client
   ```

### Publishing Locally

```bash
make local-publish
```

### Installing from Local PyPI

```bash
pip install --index-url http://pypi.ix/root/dev/+simple/ spec_objects_safety
```

---

## 📜 Design Philosophy

- Native Poetry-based development (no Docker required for development)
- Isolated Poetry virtualenv (no global pip pollution)
- Direct uploads to Artifact Registry using correct PyPI-style authentication
- Always source-driven — no hand-editing built artifacts
- Dynamic, Git-tag-based versioning
- Clear Makefile and CI workflows matching production standards

---
