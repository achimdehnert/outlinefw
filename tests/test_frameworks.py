"""Tests fuer outlinefw.frameworks"""
from outlinefw.frameworks import FRAMEWORKS, get_framework, list_frameworks


def test_all_frameworks_present():
    assert "three_act" in FRAMEWORKS
    assert "save_the_cat" in FRAMEWORKS
    assert "heros_journey" in FRAMEWORKS
    assert "five_act" in FRAMEWORKS
    assert "dan_harmon" in FRAMEWORKS


def test_framework_has_required_keys():
    for key, fw in FRAMEWORKS.items():
        assert "name" in fw
        assert "description" in fw
        assert "beats" in fw
        assert "beat_details" in fw
        assert len(fw["beats"]) > 0
        assert len(fw["beat_details"]) > 0


def test_beat_details_positions():
    for key, fw in FRAMEWORKS.items():
        for beat in fw["beat_details"]:
            assert 0.0 <= beat["position"] <= 1.0
            assert beat["tension"] in ("low", "medium", "high", "peak")


def test_get_framework_fallback():
    fw = get_framework("nonexistent")
    assert fw["name"] == "Drei-Akt-Struktur"


def test_list_frameworks_count():
    result = list_frameworks()
    assert len(result) == 5
    keys = [f["key"] for f in result]
    assert "save_the_cat" in keys
    assert "dan_harmon" in keys
