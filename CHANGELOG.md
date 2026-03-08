# Changelog

All notable changes to `iil-outlinefw` are documented here.

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
