"""
outlinefw/src/outlinefw/generator.py

OutlineGenerator -- orchestrates LLM call + parse_nodes().
Always returns OutlineResult, never raises.

Prompt Architecture (ADR-001):
  One unified system prompt. User prompt is built dynamically from:
    1. Framework structure (beats overview from FrameworkDefinition)
    2. Full ProjectContext (all non-empty fields injected)
    3. Framework-specific instructions (FrameworkDefinition.llm_instructions)
  content_mode routes to the appropriate context labeling (fiction vs. nonfiction)
  but does NOT restrict which fields are available.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Protocol, runtime_checkable

from outlinefw.frameworks import get_framework
from outlinefw.parser import parse_nodes
from outlinefw.schemas import (
    FrameworkDefinition,
    GenerationStatus,
    LLMQuality,
    OutlineResult,
    ParseStatus,
    ProjectContext,
)

logger = logging.getLogger(__name__)


class LLMRouterError(Exception):
    """Raised by LLMRouter.completion() on unrecoverable failure."""

    pass


class LLMRouterTimeout(LLMRouterError):
    """Raised when LLM call exceeds the allowed timeout."""

    pass


@runtime_checkable
class LLMRouter(Protocol):
    """
    Structural protocol for LLM routing.
    Compatible with iil-aifw and any custom router.
    """

    def completion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str: ...


@runtime_checkable
class AsyncLLMRouter(Protocol):
    """Async structural protocol for LLM routing."""

    async def acompletion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str: ...


# Single unified system prompt — content-type agnostic
_SYSTEM_PROMPT = """\
Du bist ein professioneller Outline-Assistent fuer alle Textformate.
Du erstellst strukturierte Gliederungen fuer Romane, Sachbuecher, wissenschaftliche Arbeiten,
Essays, Drehbuecher und alle anderen Textformen.
Antworte AUSSCHLIESSLICH mit einem JSON-Array. Kein Text davor oder danach.

Jedes Objekt im Array muss diese Felder enthalten:
- beat_name: string (Identifier aus dem Framework)
- position: float (0.0 bis 1.0)
- act: string (act_1 | act_2a | act_2b | act_3 | act_open | act_close)
- title: string (praegnanter Titel fuer diesen Abschnitt)
- summary: string (150-300 Zeichen, konkreter Inhalt fuer dieses spezifische Dokument)
- tension: string (low | medium | high | peak)
- key_events: array of strings (2-4 konkrete Punkte/Ereignisse/Argumente)
"""

# Legacy alias
_FICTION_SYSTEM_PROMPT = _SYSTEM_PROMPT
_NONFICTION_SYSTEM_PROMPT = _SYSTEM_PROMPT


def _format_context_block(framework: FrameworkDefinition, context: ProjectContext) -> str:
    """Build a complete context block from ALL available ProjectContext fields.

    Every non-empty field is included so the LLM has maximum information.
    Labels adapt to content_mode for natural language fit.
    """
    is_nonfiction = framework.content_mode == "nonfiction"
    lines: list[str] = []

    lines.append(f"- Titel: {context.title}")
    lines.append(f"- Format/Genre: {context.genre}")

    if is_nonfiction:
        lines.append(f"- Kernaussage/These: {context.logline}")
    else:
        lines.append(f"- Logline: {context.logline}")

    if context.research_question:
        lines.append(f"- Forschungsfrage: {context.research_question}")
    if context.methodology:
        lines.append(f"- Methodik/Ansatz: {context.methodology}")

    if not is_nonfiction:
        if context.protagonist:
            lines.append(f"- Protagonist: {context.protagonist}")
        if context.setting:
            lines.append(f"- Setting: {context.setting}")

    if context.themes:
        lines.append(f"- Themen: {', '.join(context.themes)}")
    if context.tone:
        lines.append(f"- Ton/Stil: {context.tone}")
    if context.target_word_count:
        lines.append(f"- Zielumfang: ca. {context.target_word_count:,} Woerter")
    if context.additional_notes:
        lines.append(f"- Weitere Hinweise: {context.additional_notes}")

    lines.append(f"- Ausgabesprache: {context.language_code}")
    return "\n".join(lines)


def _build_user_prompt(framework: FrameworkDefinition, context: ProjectContext) -> str:
    """Build a fully dynamic user prompt from framework structure + full context.

    Uses ALL available ProjectContext fields. Framework-specific instructions
    (llm_instructions) are appended last for maximum influence.
    """
    beats_overview = "\n".join(
        f"  {i + 1}. [{b.position:.2f}] {b.name}: {b.description}"
        for i, b in enumerate(framework.beats)
    )
    context_block = _format_context_block(framework, context)

    section_label = "Abschnitte" if framework.content_mode == "nonfiction" else "Beats"

    prompt = f"""\
Format/Framework: {framework.name}
Beschreibung: {framework.description}

{section_label} in Reihenfolge:
{beats_overview}

Projekt-Kontext:
{context_block}

Erstelle jetzt das vollstaendige JSON-Array mit allen {len(framework.beats)} {section_label}.
Jeder Eintrag muss konkret auf dieses spezifische Dokument zugeschnitten sein.
"""

    if framework.llm_instructions:
        prompt += f"\nSpezifische Anforderungen fuer dieses Format:\n{framework.llm_instructions}\n"

    return prompt


def _get_system_prompt(framework: FrameworkDefinition) -> str:
    """Return system prompt: framework override > unified default."""
    return framework.system_prompt or _SYSTEM_PROMPT


# Legacy helpers (backward compat)
def _build_fiction_user_prompt(framework: FrameworkDefinition, context: ProjectContext) -> str:
    return _build_user_prompt(framework, context)


def _build_nonfiction_user_prompt(framework: FrameworkDefinition, context: ProjectContext) -> str:
    return _build_user_prompt(framework, context)


def _build_result(
    raw_response: str,
    framework_key: str,
    framework: FrameworkDefinition,
    context: ProjectContext,
    start_ms: int,
) -> OutlineResult:
    """Parse raw LLM response and build OutlineResult."""
    parse_result = parse_nodes(raw_response)
    elapsed_ms = int(time.time() * 1000) - start_ms

    base: dict[str, Any] = {
        "framework_key": framework_key,
        "framework_name": framework.name,
        "project_title": context.title,
        "raw_llm_response": raw_response,
        "parse_result": parse_result,
        "total_beats": len(framework.beats),
        "generation_time_ms": elapsed_ms,
    }

    if parse_result.status == ParseStatus.SUCCESS:
        return OutlineResult(
            status=GenerationStatus.SUCCESS,
            nodes=parse_result.nodes,
            generated_beats=len(parse_result.nodes),
            **base,
        )
    if parse_result.status == ParseStatus.PARTIAL:
        return OutlineResult(
            status=GenerationStatus.PARTIAL,
            nodes=parse_result.nodes,
            generated_beats=len(parse_result.nodes),
            error_message=parse_result.error_message,
            **base,
        )
    if parse_result.status == ParseStatus.EMPTY:
        return OutlineResult(
            status=GenerationStatus.PARSE_ERROR,
            error_message=f"LLM returned empty response: {parse_result.error_message}",
            generated_beats=0,
            **base,
        )
    return OutlineResult(
        status=GenerationStatus.PARSE_ERROR,
        error_message=parse_result.error_message,
        generated_beats=0,
        **base,
    )


def _error_result(
    status: GenerationStatus,
    framework_key: str,
    framework_name: str,
    project_title: str,
    error_message: str,
    total_beats: int,
    start_ms: int,
) -> OutlineResult:
    return OutlineResult(
        status=status,
        framework_key=framework_key,
        framework_name=framework_name,
        project_title=project_title,
        error_message=error_message,
        total_beats=total_beats,
        generation_time_ms=int(time.time() * 1000) - start_ms,
    )


class OutlineGenerator:
    """
    Generates outlines for any text format by calling an LLMRouter and parsing the response.

    The prompt is built dynamically from:
    - FrameworkDefinition (structure, beats, llm_instructions)
    - ProjectContext (all available fields)

    Usage:
        generator = OutlineGenerator(router=my_router)
        result = generator.generate("scientific_essay", context=ProjectContext(...))
        result = generator.generate("save_the_cat", context=ProjectContext(...))
    """

    def __init__(self, router: LLMRouter | AsyncLLMRouter) -> None:
        if not isinstance(router, (LLMRouter, AsyncLLMRouter)):
            raise TypeError(
                f"router must implement LLMRouter or AsyncLLMRouter Protocol. "
                f"Got: {type(router).__name__}"
            )
        self._router = router

    def generate(
        self,
        framework_key: str,
        context: ProjectContext,
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> OutlineResult:
        """Generate a complete outline. Always returns OutlineResult, never raises."""
        if not isinstance(self._router, LLMRouter):
            raise TypeError("Sync generate() requires a router implementing LLMRouter.completion()")

        start_ms = int(time.time() * 1000)

        try:
            framework = get_framework(framework_key)
        except KeyError as e:
            return _error_result(
                GenerationStatus.VALIDATION_ERROR, framework_key, "",
                context.title, str(e), 0, start_ms,
            )

        messages = [
            {"role": "system", "content": _get_system_prompt(framework)},
            {"role": "user", "content": _build_user_prompt(framework, context)},
        ]

        try:
            raw_response = self._router.completion(
                action_code="outline.generate",
                messages=messages,
                quality=quality,
                priority=priority,
            )
        except LLMRouterTimeout as e:
            logger.warning("LLM timeout: %s", e)
            return _error_result(
                GenerationStatus.LLM_ERROR, framework_key, framework.name,
                context.title, f"LLM timeout: {e}", len(framework.beats), start_ms,
            )
        except LLMRouterError as e:
            logger.error("LLM error: %s", e)
            return _error_result(
                GenerationStatus.LLM_ERROR, framework_key, framework.name,
                context.title, str(e), len(framework.beats), start_ms,
            )

        return _build_result(raw_response, framework_key, framework, context, start_ms)

    async def agenerate(
        self,
        framework_key: str,
        context: ProjectContext,
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> OutlineResult:
        """Async variant of generate()."""
        if not isinstance(self._router, AsyncLLMRouter):
            raise TypeError(
                "Async agenerate() requires a router implementing AsyncLLMRouter.acompletion()"
            )

        start_ms = int(time.time() * 1000)

        try:
            framework = get_framework(framework_key)
        except KeyError as e:
            return _error_result(
                GenerationStatus.VALIDATION_ERROR, framework_key, "",
                context.title, str(e), 0, start_ms,
            )

        messages = [
            {"role": "system", "content": _get_system_prompt(framework)},
            {"role": "user", "content": _build_user_prompt(framework, context)},
        ]

        try:
            raw_response = await self._router.acompletion(
                action_code="outline.generate",
                messages=messages,
                quality=quality,
                priority=priority,
            )
        except LLMRouterTimeout as e:
            logger.warning("LLM timeout (async): %s", e)
            return _error_result(
                GenerationStatus.LLM_ERROR, framework_key, framework.name,
                context.title, f"LLM timeout: {e}", len(framework.beats), start_ms,
            )
        except LLMRouterError as e:
            logger.error("LLM error (async): %s", e)
            return _error_result(
                GenerationStatus.LLM_ERROR, framework_key, framework.name,
                context.title, str(e), len(framework.beats), start_ms,
            )

        return _build_result(raw_response, framework_key, framework, context, start_ms)
