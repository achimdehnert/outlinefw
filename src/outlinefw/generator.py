"""
outlinefw.generator -- OutlineGenerator

Framework-agnostischer Outline-Generator. Kein Django, kein DB.
"""
from __future__ import annotations

import logging
from typing import Protocol

from .frameworks import get_framework
from .parser import parse_nodes
from .schemas import OutlineResult, ProjectContext

logger = logging.getLogger(__name__)


class LLMRouter(Protocol):
    def completion(self, action_code: str, messages: list[dict],
                   quality_level: int | None = None, priority: str = "balanced") -> str: ...


class OutlineGenerator:
    def __init__(self, router: LLMRouter):
        self._router = router

    def generate(self, context: ProjectContext, framework: str = "three_act",
                 chapter_count: int = 12, quality_level: int | None = None) -> OutlineResult:
        fw = get_framework(framework)
        messages = [
            {"role": "system", "content": (
                f"Du bist ein Buchstruktur-Experte. Erstelle eine Outline nach der {fw['name']}-Methode.\n\n"
                + context.to_prompt_block()
            )},
            {"role": "user", "content": (
                f"Erstelle eine Outline mit genau {chapter_count} Kapiteln/Beats "
                f"nach der {fw['name']}-Struktur ({fw['description']}).\n\n"
                f"Framework-Beats als Orientierung: {', '.join(fw['beats'])}\n\n"
                'Gib ein JSON-Array zurueck: [{"order": 1, "title": "...", "description": "2-3 Saetze", '
                '"beat_type": "chapter", "beat": "...", "act": "act_1", "emotional_arc": "...", "notes": ""}, ...]\n\n'
                f"Exakt {chapter_count} Eintraege. Nur JSON."
            )},
        ]
        try:
            raw = self._router.completion("outline_generate", messages, quality_level=quality_level, priority="quality")
            nodes = parse_nodes(raw)
            if not nodes:
                return OutlineResult(success=False, framework=framework, error="LLM-Antwort enthielt keine gueltigen Nodes.")
            return OutlineResult(success=True, nodes=nodes, framework=framework)
        except Exception as exc:
            logger.error("OutlineGenerator.generate Fehler: %s", exc)
            return OutlineResult(success=False, framework=framework, error=str(exc))

    def expand_beat(self, context: ProjectContext, beat_title: str, beat_description: str = "",
                    sub_count: int = 3, quality_level: int | None = None) -> OutlineResult:
        messages = [
            {"role": "system", "content": "Du bist ein Buchstruktur-Experte.\n\n" + context.to_prompt_block()},
            {"role": "user", "content": (
                f"Beat: {beat_title}\n"
                + (f"Beschreibung: {beat_description}\n" if beat_description else "")
                + f"\nErarbeite {sub_count} konkrete Szenen."
                ' [{"order": 1, "title": "...", "description": "...", "beat_type": "scene"}]'
            )},
        ]
        try:
            raw = self._router.completion("outline_beat_expand", messages, quality_level=quality_level)
            return OutlineResult(success=True, nodes=parse_nodes(raw))
        except Exception as exc:
            logger.error("OutlineGenerator.expand_beat Fehler: %s", exc)
            return OutlineResult(success=False, error=str(exc))

    @staticmethod
    def context_from_dict(data: dict) -> ProjectContext:
        return ProjectContext(**{k: v for k, v in data.items() if k in ProjectContext.model_fields})
