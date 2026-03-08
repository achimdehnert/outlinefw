"""Tests fuer outlinefw.parser"""
from outlinefw.parser import parse_nodes


def test_parse_clean_json():
    raw = '[{"order": 1, "title": "Setup", "description": "Welt etablieren", "beat_type": "chapter"}]'
    nodes = parse_nodes(raw)
    assert len(nodes) == 1
    assert nodes[0].title == "Setup"
    assert nodes[0].order == 1


def test_parse_fenced_json():
    raw = '```json\n[{"order": 1, "title": "Catalyst"}]\n```'
    nodes = parse_nodes(raw)
    assert len(nodes) == 1
    assert nodes[0].title == "Catalyst"


def test_parse_with_think_tags():
    raw = '<think>Ich denke nach...</think>\n[{"order": 1, "title": "Midpoint"}]'
    nodes = parse_nodes(raw)
    assert len(nodes) == 1
    assert nodes[0].title == "Midpoint"


def test_parse_with_leading_text():
    raw = 'Hier ist die Outline:\n[{"order": 1, "title": "Resolution"}]'
    nodes = parse_nodes(raw)
    assert len(nodes) == 1


def test_parse_invalid_returns_empty():
    assert parse_nodes("Das ist kein JSON") == []


def test_parse_multiple_nodes():
    raw = '[{"order": 1, "title": "A"}, {"order": 2, "title": "B"}, {"order": 3, "title": "C"}]'
    nodes = parse_nodes(raw)
    assert len(nodes) == 3
    assert nodes[2].title == "C"
