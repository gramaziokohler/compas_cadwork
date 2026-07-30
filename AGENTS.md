# AGENTS.md

This file provides agent-agnostic setup instructions, coding conventions, and architectural context for AI coding agents and automated collaborators working on the `compas_cadwork` codebase.
It defines the standard patterns and guidelines required to maintain consistency, quality, and correctness across the project.

## What This Repository Does

`compas_cadwork` is a Python package that integrates the [COMPAS](https://compas.dev/) framework with [cadwork 3d](https://www.cadwork.com/).
It wraps cadwork's Python API ([`cwapi3d`](https://docs.cadwork.com/projects/cwapi3dpython/)) to expose COMPAS-compatible geometry kernels, data structures, and algorithms for AEC/timber workflows.

- **Target Python Version**: Python 3.14+ for development, Python 3.12+ for end-users of the library
- **Build System**: Hatchling
- **Package Manager**: [Astral uv](https://docs.astral.sh/uv/)

## Environment & Commands

All development commands are run from the repository root using `uv`.

- **Setup environment**: `uv sync`
- **Lint & type-check**: `uv run inv lint` *(Runs Ruff, strict mypy, pre-commit hooks)*
- **Run unit tests**: `uv run inv pytest` *(Runs offline pytest suite with mocked Cadwork APIs)*
- **Build documentation**: `uv run inv docs`
- **Build package**: `uv build`

## Code Style & Implementation Guidelines

### Imports

- Prefer absolute imports for package references.

    Example: `from compas_cadwork.a.b import Something`

- Use relative imports *only* when importing another file within the **same** module.

    Example: `from .something import Something`

### Typing & Modern Python Standards

- Target modern Python with strict typing.

- Do not use deprecated typing aliases from `typing`, prefer standard library collections.

    Example: Use `from collections.abc import Iterator`, never `from typing import Iterator`

- Prefer `typing` over `typing_extensions` unless the feature is unavailable in the project's target Python version.

### Simplicity & Cleanliness

- Keep code simple, concise, and easy for humans to read.
- Do not add unnecessary comments. Follow existing conventions in the file you are editing.
- **Carefully inspect comments and pydoc for typos and type mismatches.** If linters miss a typo or mismatch in docstrings/comments, it is your responsibility to catch it.
- **Never use classes, functions, or modules marked `@deprecated`.** Deprecated elements exist solely for backwards compatibility during refactoring.

## Architecture & Project Structure

```
├── src/compas_cadwork/
│   ├── __init__.py          # Version definition
│   ├── project.py           # Project class (main entrypoint)
│   ├── elements/            # Element hierarchy & factory
│   ├── materials/           # Material, Layer, LayerStack
│   └── conversions/         # COMPAS <-> cadwork primitive conversions
├── tests/
│   ├── conftest.py          # Fixtures & mocks for Cadwork APIs
│   └── compas_cadwork/      # Test suite mirroring src/
├── docs/                    # MkDocs source files
├── mkdocs.yml               # MkDocs configuration
├── pyproject.toml           # Project & tool config
└── tasks.py                 # Invoke tasks definition
```

### Mocking Cadwork APIs

Unit tests mock the [Cadwork APIs](https://docs.cadwork.com/projects/cwapi3dpython/) so tests run headlessly on Linux/macOS without Cadwork 3D installed.
Refer to `tests/conftest.py` to see how mocks and fixtures are constructed when writing or modifying tests.

### Documentation Requirements

- Project documentation is written using MkDocs (`docs/` directory and root `mkdocs.yml`).
- Always update the API reference in documentation when adding a new module.
- Add clear example usage for any new complex features.

## Verification & PR Checklist

Before completing any task:

1. Run `uv sync` to ensure your virtual environment is up to date.
2. Run `uv run inv lint` and verify all linters and strict `mypy` checks pass.
3. Run `uv run inv pytest` to ensure all tests pass.
4. Confirm no `@deprecated` components were imported or used.
5. Update `docs/` and `mkdocs.yml` for new modules or complex features.
6. Ensure `CHANGELOG.md` has an entry under `## Unreleased`.
