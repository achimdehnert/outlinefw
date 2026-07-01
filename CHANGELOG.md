# Changelog

All notable changes to `iil-outlinefw` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Fixed
- `OutlineGenerator.generate()`/`agenerate()` now honour their "never raises" contract for
  *any* router exception — a non-`LLMRouterError`/`Timeout` exception (e.g. `ValueError`, raw
  `httpx` errors) is caught and mapped to `GenerationStatus.LLM_ERROR` instead of propagating.
- `__version__` is now derived from installed package metadata (`importlib.metadata`) instead of
  a hand-maintained literal that had drifted to `0.3.1` behind the packaged `0.3.2`.
- README Quick-Start updated to the real `generate(framework_key, context)` signature and the
  actual `OutlineNode` fields (`position`, `beat_name`) — the previous example raised `TypeError`.
- Resolved the 5 outstanding `mypy --strict` errors (3× `no-any-return` in `parser`/`client`,
  2× implicit-reexport `attr-defined`); the `Typing :: Typed` classifier is now truthful.

### Changed
- Python support unified on 3.12: dropped stale 3.10/3.11 classifiers and bumped ruff
  `target-version`/mypy `python_version` to match `requires-python = ">=3.12"`. Status enums
  migrated to `enum.StrEnum` accordingly.
- `KnowledgeSettings.api_token` is now a `pydantic.SecretStr` so the Outline bearer token no
  longer leaks through `repr()`/logs/tracebacks.

### Added
- Makefile `format`, `mypy`, and `check` targets (`check` = lint + mypy + test, mirroring CI).
- CI: `build` job (`python -m build` + `twine check`), `typecheck` job (`mypy --strict`), and
  pip caching on all jobs.
- Tests for previously-uncovered error paths: unexpected-router-exception, sync-router-into-
  `agenerate()`, `SCHEMA_MISMATCH` branches, and `OutlineWikiClient.update_document()`/`close()`.

---

## [0.3.2] — 2026-04-28

### Fixed
- Packaging metadata: added `[project.urls]` table (Homepage, Repository, Issues)
- `hatch.build.targets.wheel` packages path corrected to `src/outlinefw`
- `pyproject.toml` classifiers updated to reflect MIT licence
- Ruff target-version and import-sort `known-first-party` aligned with `src/` layout

---

## [0.3.1] — 2026-04-10

### Fixed
- `pytest.ini_options`: `asyncio_mode = "auto"` added — eliminates `PytestUnraisableExceptionWarning` in async tests
- `coverage.run.omit` now excludes `tests/*` from coverage report
- Ruff lint ruleset extended (`N`, `UP`, `B`, `C4`, `SIM`, `RUF`) for stricter compliance

---

## [0.3.0] — 2026-03-30

### Added
- `requires-python = ">=3.12"` — aligns with platform standard
- Platform workflow sync (.windsurf rules)
- MIT LICENSE

### Changed
- `full` extra now aggregates `django`, `knowledge`, `dev`

---

## [0.2.0] - 2026-03-24

### Added
- `generator.py`: `AsyncLLMRouter` Protocol + `OutlineGenerator.agenerate()` async method
- `frameworks.py`: `register_framework()` + `unregister_framework()` for extensible registry
- `export.py`: `to_markdown()`, `to_json()`, `to_dict()` export functions
- `knowledge/client.py`: `OutlineWikiClient` — async HTTP client for Outline Wiki REST API
- `knowledge/settings.py`: `KnowledgeSettings` — pydantic-settings with `OUTLINE_` env prefix
- `knowledge/enrichment.py`: `enrich_context()` — feed Wiki research into OutlineGenerator
- `tests/conftest.py`: Shared fixtures and mock routers (sync + async)
- `tests/test_export.py`: 12 export tests (Markdown, JSON, dict)
- `tests/test_registry.py`: 5 framework registry tests
- `tests/test_async_generator.py`: 6 async generator tests
- `tests/test_knowledge.py`: 15 knowledge module tests (client, settings, enrichment)
- `pyproject.toml`: `[knowledge]` optional extra (httpx, pydantic-settings, tenacity)
- `pyproject.toml`: `asyncio_mode = "auto"` for pytest-asyncio

### Changed
- `generator.py`: Extracted `_build_result()` + `_error_result()` helpers (DRY)
- `generator.py`: `OutlineGenerator.__init__` accepts `LLMRouter | AsyncLLMRouter`
- `__init__.py`: Exports `AsyncLLMRouter`, `register_framework`, `unregister_framework`, export functions
- Test count: 50 → 98 tests

---

## [0.1.1] - 2026-03-08

### Fixed
- Ruff lint + format compliance for CI

---

## [0.1.0] - 2026-03-08

### Added
- `schemas.py`: `ActPhase`, `TensionLevel`, `LLMQuality`, `GenerationStatus`, `ParseStatus` enums
- `schemas.py`: `BeatDefinition`, `FrameworkDefinition` with full position validation
- `schemas.py`: `ProjectContext`, `OutlineNode`, `OutlineResult` with `completion_ratio` + `raise_if_failed()`
- `frameworks.py`: 5 frameworks — Three-Act, Save the Cat, Hero's Journey, Five-Act, Dan Harmon Story Circle
- `generator.py`: `LLMRouter` Protocol (`@runtime_checkable`) with `LLMRouterError` + `LLMRouterTimeout`
- `generator.py`: `OutlineGenerator` — always returns `OutlineResult`, never raises
- `parser.py`: `parse_nodes()` — robust LLM JSON parser
- `django_adapter.py`: `OutlineServiceBase` ABC + `InMemoryOutlineService` for testing
- `py.typed` marker for PEP 561 compliance
- Full test suite: 30+ tests
