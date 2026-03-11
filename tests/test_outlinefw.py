"""
tests/test_outlinefw.py

Production test suite for iil-outlinefw.

Covers:
  - schemas.py: Beat position validation, OutlineResult states
  - frameworks.py: All 5 frameworks pass validation, versioned
  - parser.py: All ParseStatus outcomes with real LLM-like inputs
  - generator.py: LLMRouter Protocol, error propagation
  - django_adapter.py: ABC enforcement, InMemoryOutlineService

Run: pytest tests/test_outlinefw.py -v --tb=short
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from outlinefw.django_adapter import InMemoryOutlineService, OutlineServiceBase
from outlinefw.frameworks import (
    DAN_HARMON,
    FIVE_ACT,
    FRAMEWORKS,
    HEROS_JOURNEY,
    SAVE_THE_CAT,
    THREE_ACT,
    get_framework,
    list_frameworks,
)
from outlinefw.generator import LLMRouterError, LLMRouterTimeout, OutlineGenerator
from outlinefw.parser import _preprocess, parse_nodes
from outlinefw.schemas import (
    ActPhase,
    BeatDefinition,
    FrameworkDefinition,
    GenerationStatus,
    LLMQuality,
    OutlineGenerationError,
    OutlineResult,
    ParseStatus,
    ProjectContext,
    TensionLevel,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_context() -> ProjectContext:
    return ProjectContext(
        title="Der Verrat",
        genre="Thriller",
        logline="Ein Detektiv entdeckt, dass sein Partner ein Maulwurf ist.",
        protagonist="Kommissar Berger",
        setting="Muenchen, Gegenwart",
        themes=["Verrat", "Loyalitaet"],
        tone="dunkel, spannungsgeladen",
        language_code="de",
    )


def _make_nodes_json(framework: FrameworkDefinition) -> str:
    nodes = [
        {
            "beat_name": beat.name,
            "position": beat.position,
            "act": beat.act.value,
            "title": f"Titel fuer {beat.name}",
            "summary": f"Zusammenfassung fuer den Beat '{beat.name}' mit ausreichend Text.",
            "tension": beat.tension.value,
            "key_events": ["Ereignis A", "Ereignis B"],
        }
        for beat in framework.beats
    ]
    return json.dumps(nodes)


class GoodRouter:
    def __init__(self, framework_key: str = "three_act") -> None:
        self._fw = get_framework(framework_key)

    def completion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        return _make_nodes_json(self._fw)


class ErrorRouter:
    def completion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        raise LLMRouterError("simulated LLM failure")


class TimeoutRouter:
    def completion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        raise LLMRouterTimeout("simulated timeout")


class EmptyRouter:
    def completion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        return ""


# ---------------------------------------------------------------------------
# Schema Tests
# ---------------------------------------------------------------------------


class TestBeatDefinition:
    def test_valid_beat(self) -> None:
        beat = BeatDefinition(
            name="setup",
            position=0.0,
            act=ActPhase.ACT_1,
            description="Setup beat.",
            tension=TensionLevel.LOW,
        )
        assert beat.name == "setup"
        assert beat.position == 0.0

    def test_position_rounded_to_2dp(self) -> None:
        beat = BeatDefinition(
            name="test",
            position=0.123456789,
            act=ActPhase.ACT_1,
            description="x",
            tension=TensionLevel.LOW,
        )
        assert beat.position == 0.12

    def test_frozen(self) -> None:
        beat = BeatDefinition(
            name="x", position=0.0, act=ActPhase.ACT_1, description="x", tension=TensionLevel.LOW
        )
        with pytest.raises((TypeError, Exception)):
            beat.name = "y"  # type: ignore[misc]


class TestFrameworkDefinition:
    def test_duplicate_positions_rejected(self) -> None:
        with pytest.raises(ValueError, match="duplicate beat positions"):
            FrameworkDefinition(
                key="test_fw",
                name="Test",
                description="Test framework",
                beats=[
                    BeatDefinition(
                        name="a",
                        position=0.0,
                        act=ActPhase.ACT_1,
                        description="a",
                        tension=TensionLevel.LOW,
                    ),
                    BeatDefinition(
                        name="b",
                        position=0.0,
                        act=ActPhase.ACT_1,
                        description="b",
                        tension=TensionLevel.LOW,
                    ),
                    BeatDefinition(
                        name="c",
                        position=1.0,
                        act=ActPhase.ACT_3,
                        description="c",
                        tension=TensionLevel.LOW,
                    ),
                ],
            )

    def test_unsorted_positions_rejected(self) -> None:
        with pytest.raises(ValueError, match="ordered by position"):
            FrameworkDefinition(
                key="test_fw",
                name="Test",
                description="Test framework",
                beats=[
                    BeatDefinition(
                        name="a",
                        position=0.5,
                        act=ActPhase.ACT_1,
                        description="a",
                        tension=TensionLevel.LOW,
                    ),
                    BeatDefinition(
                        name="b",
                        position=0.0,
                        act=ActPhase.ACT_1,
                        description="b",
                        tension=TensionLevel.LOW,
                    ),
                    BeatDefinition(
                        name="c",
                        position=1.0,
                        act=ActPhase.ACT_3,
                        description="c",
                        tension=TensionLevel.LOW,
                    ),
                ],
            )

    def test_excessive_gap_rejected(self) -> None:
        with pytest.raises(ValueError, match="gap of"):
            FrameworkDefinition(
                key="test_fw",
                name="Test",
                description="Test framework",
                beats=[
                    BeatDefinition(
                        name="a",
                        position=0.0,
                        act=ActPhase.ACT_1,
                        description="a",
                        tension=TensionLevel.LOW,
                    ),
                    BeatDefinition(
                        name="b",
                        position=0.5,
                        act=ActPhase.ACT_2A,
                        description="b",
                        tension=TensionLevel.LOW,
                    ),
                    BeatDefinition(
                        name="c",
                        position=1.0,
                        act=ActPhase.ACT_3,
                        description="c",
                        tension=TensionLevel.LOW,
                    ),
                ],
            )


class TestOutlineResult:
    def test_success_property(self) -> None:
        result = OutlineResult(
            status=GenerationStatus.SUCCESS,
            framework_key="three_act",
            framework_name="Drei-Akt",
            project_title="Test",
        )
        assert result.success is True

    def test_raise_if_failed(self) -> None:
        result = OutlineResult(
            status=GenerationStatus.PARSE_ERROR,
            framework_key="three_act",
            framework_name="Drei-Akt",
            project_title="Test",
            error_message="bad JSON",
        )
        with pytest.raises(OutlineGenerationError, match="bad JSON"):
            result.raise_if_failed()

    def test_completion_ratio(self) -> None:
        result = OutlineResult(
            status=GenerationStatus.PARTIAL,
            framework_key="three_act",
            framework_name="Drei-Akt",
            project_title="Test",
            total_beats=7,
            generated_beats=5,
        )
        assert result.completion_ratio == pytest.approx(5 / 7)


# ---------------------------------------------------------------------------
# Framework Tests
# ---------------------------------------------------------------------------


class TestFrameworks:
    @pytest.mark.parametrize(
        "framework", [THREE_ACT, SAVE_THE_CAT, HEROS_JOURNEY, FIVE_ACT, DAN_HARMON]
    )
    def test_framework_validates(self, framework: FrameworkDefinition) -> None:
        assert framework.key != ""
        assert len(framework.beats) >= 2

    @pytest.mark.parametrize(
        "key,expected_beats",
        [
            ("three_act", 7),
            ("save_the_cat", 15),
            ("heros_journey", 12),
            ("five_act", 5),
            ("dan_harmon", 8),
        ],
    )
    def test_beat_counts(self, key: str, expected_beats: int) -> None:
        assert len(get_framework(key).beats) == expected_beats

    def test_get_framework_unknown_raises_key_error(self) -> None:
        with pytest.raises(KeyError, match="Unknown framework key"):
            get_framework("nonexistent")

    def test_list_frameworks_has_all(self) -> None:
        listing = list_frameworks()
        assert len(listing) == 5
        assert "dan_harmon" in {f["key"] for f in listing}

    def test_framework_has_version(self) -> None:
        for fw in FRAMEWORKS.values():
            assert fw.version

    def test_positions_monotone(self) -> None:
        for fw in FRAMEWORKS.values():
            positions = [b.position for b in fw.beats]
            assert positions == sorted(positions)


# ---------------------------------------------------------------------------
# Parser Tests
# ---------------------------------------------------------------------------


class TestPreprocess:
    def test_strips_json_fence(self) -> None:
        assert _preprocess("```json\n[]\n```") == "[]"

    def test_fixes_trailing_comma(self) -> None:
        assert _preprocess('{"key": "val",}') == '{"key": "val"}'

    def test_fixes_python_booleans(self) -> None:
        result = _preprocess('{"flag": True, "other": False, "null": None}')
        assert "true" in result and "false" in result and "null" in result


class TestParseNodes:
    def test_success(self) -> None:
        result = parse_nodes(_make_nodes_json(THREE_ACT))
        assert result.status == ParseStatus.SUCCESS
        assert len(result.nodes) == 7

    def test_empty(self) -> None:
        assert parse_nodes("").status == ParseStatus.EMPTY

    def test_malformed_json(self) -> None:
        assert parse_nodes("{not: valid}").status == ParseStatus.MALFORMED_JSON

    def test_fenced_json(self) -> None:
        raw = f"```json\n{_make_nodes_json(THREE_ACT)}\n```"
        assert parse_nodes(raw).status == ParseStatus.SUCCESS

    def test_wrapped_in_outline_key(self) -> None:
        nodes = json.loads(_make_nodes_json(THREE_ACT))
        result = parse_nodes(json.dumps({"outline": nodes}))
        assert result.status == ParseStatus.SUCCESS

    def test_partial_parse(self) -> None:
        # A node with position > 1.0 triggers ValidationError in OutlineNode
        nodes = json.loads(_make_nodes_json(THREE_ACT))
        nodes[2] = {
            "beat_name": "bad_node",
            "position": 99.0,  # violates ge=0.0, le=1.0
            "act": "act_1",
            "title": "Bad Node",
            "summary": "This node has an invalid position that cannot be coerced.",
            "tension": "low",
        }
        result = parse_nodes(json.dumps(nodes))
        assert result.status == ParseStatus.PARTIAL
        assert len(result.failed_nodes) == 1

    def test_act_alias(self) -> None:
        nodes = [
            {
                "beat_name": "test",
                "position": 0.0,
                "act": "act1",
                "title": "T",
                "summary": "A test summary with enough characters.",
                "tension": "low",
            }
        ]
        result = parse_nodes(json.dumps(nodes))
        assert result.status == ParseStatus.SUCCESS
        assert result.nodes[0].act == ActPhase.ACT_1


# ---------------------------------------------------------------------------
# Generator Tests
# ---------------------------------------------------------------------------


class TestOutlineGenerator:
    def test_requires_llm_router_protocol(self) -> None:
        with pytest.raises(TypeError, match="LLMRouter Protocol"):
            OutlineGenerator(router="not a router")  # type: ignore[arg-type]

    def test_successful_generation(self, sample_context: ProjectContext) -> None:
        result = OutlineGenerator(router=GoodRouter("three_act")).generate(
            "three_act", sample_context
        )
        assert result.status == GenerationStatus.SUCCESS
        assert len(result.nodes) == 7

    def test_llm_error(self, sample_context: ProjectContext) -> None:
        result = OutlineGenerator(router=ErrorRouter()).generate("three_act", sample_context)
        assert result.status == GenerationStatus.LLM_ERROR

    def test_timeout(self, sample_context: ProjectContext) -> None:
        result = OutlineGenerator(router=TimeoutRouter()).generate("three_act", sample_context)
        assert result.status == GenerationStatus.LLM_ERROR
        assert "timeout" in result.error_message.lower()

    def test_empty_response(self, sample_context: ProjectContext) -> None:
        result = OutlineGenerator(router=EmptyRouter()).generate("three_act", sample_context)
        assert result.status == GenerationStatus.PARSE_ERROR

    def test_unknown_framework(self, sample_context: ProjectContext) -> None:
        result = OutlineGenerator(router=GoodRouter()).generate("nonexistent", sample_context)
        assert result.status == GenerationStatus.VALIDATION_ERROR

    def test_result_has_timing(self, sample_context: ProjectContext) -> None:
        result = OutlineGenerator(router=GoodRouter()).generate("three_act", sample_context)
        assert result.generation_time_ms is not None and result.generation_time_ms >= 0

    def test_total_beats(self, sample_context: ProjectContext) -> None:
        result = OutlineGenerator(router=GoodRouter("save_the_cat")).generate(
            "save_the_cat", sample_context
        )
        assert result.total_beats == 15


# ---------------------------------------------------------------------------
# Django Adapter Tests
# ---------------------------------------------------------------------------


class TestOutlineServiceBaseABC:
    def test_cannot_instantiate_abstract(self) -> None:
        with pytest.raises((TypeError, Exception)):
            OutlineServiceBase()  # type: ignore[abstract]

    def test_missing_method_raises(self) -> None:
        class IncompleteService(OutlineServiceBase):
            def persist_outline(self, result: Any, context: Any, tenant_id: int) -> Any:
                pass

            def get_llm_router(self, tenant_id: int) -> Any:
                pass

        with pytest.raises((TypeError, Exception)):
            IncompleteService()


class TestInMemoryOutlineService:
    def test_generates_and_persists(self, sample_context: ProjectContext) -> None:
        service = InMemoryOutlineService(router=GoodRouter("three_act"), tenant_id=42)
        result = service.generate_and_persist("three_act", sample_context, request=None)
        assert result.success
        assert len(service.persisted) == 1
        assert service.persisted[0]["tenant_id"] == 42

    def test_no_persist_on_failure(self, sample_context: ProjectContext) -> None:
        service = InMemoryOutlineService(router=ErrorRouter(), tenant_id=1)
        result = service.generate_and_persist("three_act", sample_context, request=None)
        assert not result.success
        assert len(service.persisted) == 0
