"""Shared fixtures for outlinefw tests."""

from __future__ import annotations

import json

import pytest

from outlinefw.frameworks import get_framework
from outlinefw.generator import LLMRouterError, LLMRouterTimeout
from outlinefw.schemas import FrameworkDefinition, LLMQuality, ProjectContext


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


def make_nodes_json(framework: FrameworkDefinition) -> str:
    """Generate valid JSON response for a given framework."""
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
    """Router that returns valid JSON for a given framework."""

    def __init__(self, framework_key: str = "three_act") -> None:
        self._fw = get_framework(framework_key)

    def completion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        return make_nodes_json(self._fw)


class AsyncGoodRouter:
    """Async router that returns valid JSON for a given framework."""

    def __init__(self, framework_key: str = "three_act") -> None:
        self._fw = get_framework(framework_key)

    def completion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        return make_nodes_json(self._fw)

    async def acompletion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        return make_nodes_json(self._fw)


class ErrorRouter:
    """Router that always raises LLMRouterError."""

    def completion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        raise LLMRouterError("simulated LLM failure")

    async def acompletion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        raise LLMRouterError("simulated LLM failure")


class TimeoutRouter:
    """Router that always raises LLMRouterTimeout."""

    def completion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        raise LLMRouterTimeout("simulated timeout")

    async def acompletion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        raise LLMRouterTimeout("simulated timeout")


class EmptyRouter:
    """Router that returns empty string."""

    def completion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        return ""

    async def acompletion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str:
        return ""
