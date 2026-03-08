"""Tests fuer outlinefw.parser -- ParseResult API (v0.1.0)"""
from outlinefw.parser import parse_nodes
from outlinefw.schemas import ParseStatus


def test_parse_clean_json():
    raw = '[{"order": 1, "title": "Setup", "summary": "Welt etablieren"}]'
    result = parse_nodes(raw)
    assert result.status == ParseStatus.SUCCESS
    assert len(result.nodes) == 1
    assert result.nodes[0].title == "Setup"


def test_parse_fenced_json():
    raw = '```json\n[{"order": 1, "title": "Catalyst", "summary": "Wendepunkt"}]\n```'
    result = parse_nodes(raw)
    assert result.status == ParseStatus.SUCCESS
    assert len(result.nodes) == 1
    assert result.nodes[0].title == "Catalyst"


def test_parse_with_think_tags():
    raw = '<think>Ich denke nach...</think>\n[{"order": 1, "title": "Midpoint", "summary": "Mitte"}]'
    result = parse_nodes(raw)
    assert result.status == ParseStatus.SUCCESS
    assert len(result.nodes) == 1
    assert result.nodes[0].title == "Midpoint"


def test_parse_with_leading_text():
    raw = 'Hier ist die Outline:\n[{"order": 1, "title": "Resolution", "summary": "Ende"}]'
    result = parse_nodes(raw)
    assert result.status == ParseStatus.SUCCESS
    assert len(result.nodes) == 1


def test_parse_invalid_returns_empty():
    result = parse_nodes("Das ist kein JSON")
    assert result.status != ParseStatus.SUCCESS
    assert result.nodes == []


def test_parse_multiple_nodes():
    raw = '[{"order": 1, "title": "A", "summary": "a"}, {"order": 2, "title": "B", "summary": "b"}, {"order": 3, "title": "C", "summary": "c"}]'
    result = parse_nodes(raw)
    assert result.status == ParseStatus.SUCCESS
    assert len(result.nodes) == 3
    assert result.nodes[2].title == "C"
