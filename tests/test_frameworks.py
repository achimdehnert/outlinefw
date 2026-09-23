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
    for _key, fw in FRAMEWORKS.items():
        assert fw.name
        assert fw.description
        assert len(fw.beats) > 0


def test_beat_positions():
    for _key, fw in FRAMEWORKS.items():
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
    assert len(result) == 9
    keys = [f["key"] for f in result]
    assert "save_the_cat" in keys
    assert "dan_harmon" in keys


# ---------------------------------------------------------------------------
# scientific_essay abstract beat (writing-hub#1261 K4)
# ---------------------------------------------------------------------------

# Snapshot of beat names per framework BEFORE the abstract beat was added to
# scientific_essay. Guards against unintended changes to other frameworks
# while allowing the intentional +1 on scientific_essay.
_BEAT_NAME_SNAPSHOT = {
    "three_act": (
        "exposition",
        "inciting_incident",
        "first_turning_point",
        "midpoint",
        "second_turning_point",
        "climax",
        "resolution",
    ),
    "save_the_cat": (
        "opening_image",
        "theme_stated",
        "setup",
        "catalyst",
        "debate",
        "break_into_two",
        "b_story",
        "fun_and_games",
        "midpoint",
        "bad_guys_close_in",
        "all_is_lost",
        "dark_night_of_the_soul",
        "break_into_three",
        "finale",
        "final_image",
    ),
    "heros_journey": (
        "ordinary_world",
        "call_to_adventure",
        "refusal_of_call",
        "meeting_the_mentor",
        "crossing_the_threshold",
        "tests_allies_enemies",
        "approach_to_inmost_cave",
        "ordeal",
        "reward",
        "road_back",
        "resurrection",
        "return_with_elixir",
    ),
    "five_act": ("exposition", "rising_action", "climax", "falling_action", "denouement"),
    "dan_harmon": ("you", "need", "go", "search", "find", "take", "return", "change"),
    "academic_essay": ("einleitung", "hintergrund", "hauptteil", "gegenargumente", "schluss"),
    "imrad_article": (
        "abstract",
        "introduction",
        "methods",
        "results",
        "discussion",
        "conclusion",
    ),
    "essay": ("einstieg", "entfaltung", "vertiefung", "wende", "schluss"),
}


def test_all_frameworks_except_scientific_essay_have_unchanged_beats():
    for key, expected_names in _BEAT_NAME_SNAPSHOT.items():
        fw = get_framework(key)
        assert tuple(b.name for b in fw.beats) == expected_names, key


def test_scientific_essay_has_abstract_as_first_beat():
    fw = get_framework("scientific_essay")
    assert fw.beats[0].name == "abstract"
    assert fw.beats[0].position <= 0.1


def test_scientific_essay_beat_count_increased_by_one():
    fw = get_framework("scientific_essay")
    beat_names = [b.name for b in fw.beats]
    assert len(beat_names) == 8  # was 7 before the abstract beat
    assert beat_names == [
        "abstract",
        "einleitung",
        "forschungsstand",
        "theoretischer_rahmen",
        "hauptargument_1",
        "hauptargument_2",
        "diskussion",
        "fazit",
    ]


def test_scientific_essay_still_validates_framework_definition_rules():
    # FrameworkDefinition.validate_beat_positions (schemas.py): sorted, unique,
    # first <= 0.1, last >= 0.9, gap <= MAX_GAP (0.30). Constructing FRAMEWORKS
    # at import time already proves this; re-derive it explicitly here.
    fw = get_framework("scientific_essay")
    positions = [b.position for b in fw.beats]
    assert positions == sorted(positions)
    assert len(positions) == len(set(positions))
    assert positions[0] <= 0.1
    assert positions[-1] >= 0.9
    assert all(
        round(positions[i] - positions[i - 1], 10) <= fw.MAX_GAP for i in range(1, len(positions))
    )
