"""Tests fuer outlinefw.parser -- ParseResult API (v0.1.0)"""

import json

from outlinefw.parser import parse_nodes
from outlinefw.schemas import ParseStatus

# Minimal valid OutlineNode dicts (summary >= 10 chars)
_N1 = {
    "order": 1,
    "title": "Setup",
    "summary": "Welt etablieren und Figuren vorstellen.",
    "beat_name": "exposition",
    "act": "act_1",
    "tension": "low",
    "position": 0.0,
}
_N2 = {
    "order": 2,
    "title": "Catalyst",
    "summary": "Das ausloesende Ereignis tritt ein.",
    "beat_name": "inciting_incident",
    "act": "act_1",
    "tension": "medium",
    "position": 0.12,
}
_N3 = {
    "order": 3,
    "title": "Midpoint",
    "summary": "Falsche Niederlage oder falscher Sieg.",
    "beat_name": "midpoint",
    "act": "act_2a",
    "tension": "high",
    "position": 0.5,
}

_NODE1 = json.dumps(_N1)
_NODE2 = json.dumps(_N2)
_NODE3 = json.dumps(_N3)


def test_parse_clean_json():
    raw = f"[{_NODE1}]"
    result = parse_nodes(raw)
    assert result.status == ParseStatus.SUCCESS
    assert len(result.nodes) == 1
    assert result.nodes[0].title == "Setup"


def test_parse_fenced_json():
    raw = f"```json\n[{_NODE1}]\n```"
    result = parse_nodes(raw)
    assert result.status == ParseStatus.SUCCESS
    assert len(result.nodes) == 1
    assert result.nodes[0].title == "Setup"


def test_parse_with_think_tags():
    raw = (
        "<think>Ich analysiere die Struktur...</think>"
        f"\n[{_NODE1}]"
    )
    result = parse_nodes(raw)
    assert result.status == ParseStatus.SUCCESS
    assert len(result.nodes) == 1


def test_parse_with_leading_text():
    raw = f"Hier ist die generierte Outline:\n[{_NODE1}]"
    result = parse_nodes(raw)
    assert result.status == ParseStatus.SUCCESS
    assert len(result.nodes) == 1


def test_parse_invalid_returns_empty():
    result = parse_nodes("Das ist kein JSON")
    assert result.status != ParseStatus.SUCCESS
    assert result.nodes == []


def test_parse_multiple_nodes():
    raw = f"[{_NODE1}, {_NODE2}, {_NODE3}]"
    result = parse_nodes(raw)
    assert result.status == ParseStatus.SUCCESS
    assert len(result.nodes) == 3
    assert result.nodes[2].title == "Midpoint"
