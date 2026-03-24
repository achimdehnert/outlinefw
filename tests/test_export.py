"""Tests for outlinefw.export module."""

from __future__ import annotations

import json

from outlinefw.export import to_dict, to_json, to_markdown
from outlinefw.schemas import (
    ActPhase,
    GenerationStatus,
    OutlineNode,
    OutlineResult,
    TensionLevel,
)


def _sample_result() -> OutlineResult:
    return OutlineResult(
        status=GenerationStatus.SUCCESS,
        framework_key="three_act",
        framework_name="Drei-Akt-Struktur",
        project_title="Der Verrat",
        total_beats=7,
        generated_beats=2,
        generation_time_ms=1234,
        nodes=[
            OutlineNode(
                beat_name="exposition",
                position=0.0,
                act=ActPhase.ACT_1,
                title="Die Welt des Kommissars",
                summary="Kommissar Berger ermittelt in Muenchen.",
                tension=TensionLevel.LOW,
                key_events=["Tatort besichtigt", "Partner trifft ein"],
            ),
            OutlineNode(
                beat_name="climax",
                position=0.88,
                act=ActPhase.ACT_3,
                title="Die Konfrontation",
                summary="Berger stellt seinen Partner zur Rede.",
                tension=TensionLevel.PEAK,
                character_arcs={"Berger": "Von Vertrauen zu Misstrauen"},
            ),
        ],
    )


class TestToMarkdown:
    def test_contains_title(self) -> None:
        md = to_markdown(_sample_result())
        assert "# Der Verrat" in md

    def test_contains_framework_info(self) -> None:
        md = to_markdown(_sample_result())
        assert "Drei-Akt-Struktur" in md
        assert "three_act" in md

    def test_contains_beats(self) -> None:
        md = to_markdown(_sample_result())
        assert "Die Welt des Kommissars" in md
        assert "Die Konfrontation" in md

    def test_contains_key_events(self) -> None:
        md = to_markdown(_sample_result())
        assert "Tatort besichtigt" in md

    def test_contains_character_arcs(self) -> None:
        md = to_markdown(_sample_result())
        assert "Berger" in md
        assert "Vertrauen zu Misstrauen" in md

    def test_without_metadata(self) -> None:
        md = to_markdown(_sample_result(), include_metadata=False)
        assert "# Der Verrat" not in md
        assert "Die Welt des Kommissars" in md

    def test_contains_timing(self) -> None:
        md = to_markdown(_sample_result())
        assert "1234ms" in md


class TestToJson:
    def test_valid_json(self) -> None:
        j = to_json(_sample_result())
        data = json.loads(j)
        assert data["project_title"] == "Der Verrat"

    def test_has_nodes(self) -> None:
        data = json.loads(to_json(_sample_result()))
        assert len(data["nodes"]) == 2

    def test_without_raw(self) -> None:
        data = json.loads(to_json(_sample_result()))
        assert "raw_llm_response" not in data

    def test_with_raw(self) -> None:
        result = _sample_result().model_copy(update={"raw_llm_response": "some raw text"})
        data = json.loads(to_json(result, include_raw=True))
        assert data["raw_llm_response"] == "some raw text"


class TestToDict:
    def test_returns_dict(self) -> None:
        d = to_dict(_sample_result())
        assert isinstance(d, dict)
        assert d["status"] == "success"

    def test_completion_ratio(self) -> None:
        d = to_dict(_sample_result())
        assert d["completion_ratio"] == 0.29  # 2/7 rounded

    def test_node_structure(self) -> None:
        d = to_dict(_sample_result())
        node = d["nodes"][0]
        assert node["beat_name"] == "exposition"
        assert node["act"] == "act_1"
        assert node["tension"] == "low"
