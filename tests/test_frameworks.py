"""Tests fuer outlinefw.frameworks -- Pydantic API (v0.1.0)"""
import pytest
from outlinefw.frameworks import FRAMEWORKS, get_framework, list_frameworks


def test_all_frameworks_present():
    assert "three_act" in FRAMEWORKS
    assert "save_the_cat" in FRAMEWORKS
    assert "heros_journey" in FRAMEWORKS
    assert "five_act" in FRAMEWORKS
    assert "dan_harmon" in FRAMEWORKS


def test_framework_has_required_attributes():
    for key, fw in FRAMEWORKS.items():
        assert fw.name
        assert fw.description
        assert len(fw.beats) > 0


def test_beat_positions():
    for key, fw in FRAMEWORKS.items():
        for beat in fw.beats:
            assert 0.0 <= beat.position <= 1.0
            assert beat.tension.value in ("low", "medium", "high", "peak")


def test_get_framework_known():
    fw = get_framework("three_act")
    assert fw.name == "Drei-Akt-Struktur"


def test_get_framework_unknown_raises():
    with pytest.raises(KeyError):
        get_framework("nonexistent")


def test_list_frameworks_count():
    result = list_frameworks()
    assert len(result) == 5
    keys = [f["key"] for f in result]
    assert "save_the_cat" in keys
    assert "dan_harmon" in keys
