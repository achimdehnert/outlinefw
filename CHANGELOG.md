# Changelog

All notable changes to `iil-outlinefw` are documented here.

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

## [0.1.1] - 2026-03-08

### Fixed
- Ruff lint + format compliance for CI

## [0.1.0] - 2026-03-08

### Added
- `schemas.py`: `ActPhase`, `TensionLevel`, `LLMQuality`, `GenerationStatus`, `ParseStatus` enums
- `schemas.py`: `BeatDefinition`, `FrameworkDefinition` with full position validation (K-2)
- `schemas.py`: `ProjectContext`, `OutlineNode`, `OutlineResult` with `completion_ratio` + `raise_if_failed()` (K-3)
- `schemas.py`: `ParseResult` with 5 distinct status types (K-4)
- `frameworks.py`: 5 frameworks — Three-Act, Save the Cat, Hero's Journey, Five-Act, Dan Harmon Story Circle
- `frameworks.py`: All frameworks validated on import via `FrameworkDefinition` Pydantic model
- `generator.py`: `LLMRouter` Protocol (`@runtime_checkable`) with `LLMRouterError` + `LLMRouterTimeout` (B-2)
- `generator.py`: `OutlineGenerator` — always returns `OutlineResult`, never raises
- `parser.py`: `parse_nodes()` — robust LLM JSON parser (code fences, trailing commas, wrapper keys, act/tension aliases)
- `django_adapter.py`: `OutlineServiceBase` ABC + `InMemoryOutlineService` for testing (B-3)
- `py.typed` marker for PEP 561 compliance (K-1)
- Full test suite: `tests/test_outlinefw.py` with 30+ tests
