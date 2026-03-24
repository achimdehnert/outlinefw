"""Tests for framework registry: register_framework, unregister_framework."""

from __future__ import annotations

import pytest

from outlinefw.frameworks import (
    FRAMEWORKS,
    get_framework,
    register_framework,
    unregister_framework,
)
from outlinefw.schemas import (
    ActPhase,
    BeatDefinition,
    FrameworkDefinition,
    TensionLevel,
)


def _custom_framework(key: str = "custom_test") -> FrameworkDefinition:
    return FrameworkDefinition(
        key=key,
        name="Custom Test Framework",
        description="A minimal test framework for registry tests.",
        version="1.0.0",
        beats=[
            BeatDefinition(
                name="start",
                position=0.0,
                act=ActPhase.ACT_1,
                description="The beginning.",
                tension=TensionLevel.LOW,
            ),
            BeatDefinition(
                name="rising",
                position=0.25,
                act=ActPhase.ACT_2A,
                description="Rising action.",
                tension=TensionLevel.MEDIUM,
            ),
            BeatDefinition(
                name="middle",
                position=0.5,
                act=ActPhase.ACT_2B,
                description="The middle.",
                tension=TensionLevel.HIGH,
            ),
            BeatDefinition(
                name="falling",
                position=0.75,
                act=ActPhase.ACT_3,
                description="Falling action.",
                tension=TensionLevel.MEDIUM,
            ),
            BeatDefinition(
                name="end",
                position=1.0,
                act=ActPhase.ACT_3,
                description="The end.",
                tension=TensionLevel.LOW,
            ),
        ],
    )


class TestRegisterFramework:
    def test_register_and_retrieve(self) -> None:
        fw = _custom_framework("reg_test_1")
        try:
            register_framework(fw)
            assert get_framework("reg_test_1").name == fw.name
        finally:
            FRAMEWORKS.pop("reg_test_1", None)

    def test_duplicate_raises_value_error(self) -> None:
        fw = _custom_framework("reg_test_2")
        try:
            register_framework(fw)
            with pytest.raises(ValueError, match="already registered"):
                register_framework(fw)
        finally:
            FRAMEWORKS.pop("reg_test_2", None)


class TestUnregisterFramework:
    def test_unregister_returns_framework(self) -> None:
        fw = _custom_framework("unreg_test_1")
        try:
            register_framework(fw)
            removed = unregister_framework("unreg_test_1")
            assert removed.key == "unreg_test_1"
            assert "unreg_test_1" not in FRAMEWORKS
        finally:
            FRAMEWORKS.pop("unreg_test_1", None)

    def test_unregister_unknown_raises_key_error(self) -> None:
        with pytest.raises(KeyError, match="Unknown framework key"):
            unregister_framework("nonexistent_fw_xyz")

    def test_register_unregister_cycle(self) -> None:
        fw = _custom_framework("cycle_test")
        try:
            register_framework(fw)
            assert "cycle_test" in FRAMEWORKS
            unregister_framework("cycle_test")
            assert "cycle_test" not in FRAMEWORKS
            register_framework(fw)
            assert "cycle_test" in FRAMEWORKS
        finally:
            FRAMEWORKS.pop("cycle_test", None)
