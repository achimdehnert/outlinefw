"""
outlinefw/src/outlinefw/generator.py

OutlineGenerator -- orchestrates LLM call + parse_nodes().
Always returns OutlineResult, never raises.

LLMRouter Protocol: anything implementing completion() is compatible.
AsyncLLMRouter Protocol: async variant with acompletion().
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

    Raises:
        LLMRouterError   -- on any unrecoverable LLM failure
        LLMRouterTimeout -- on timeout
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
    """
    Async structural protocol for LLM routing.
    Compatible with iil-aifw async routers.
    """

    async def acompletion(
        self,
        action_code: str,
        messages: list[dict[str, str]],
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> str: ...


_SYSTEM_PROMPT = """\
Du bist ein professioneller Story-Struktur-Assistent.
Erstelle eine vollstaendige Story-Outline im angegebenen Framework.
Antworte AUSSCHLIESSLICH mit einem JSON-Array von Beat-Objekten.
Kein erklaerende Text, kein Markdown ausser dem JSON selbst.

Jedes Beat-Objekt muss folgende Felder enthalten:
- beat_name: string (Framework-Beat-Identifier)
- position: float (0.0 bis 1.0)
- act: string (act_1 | act_2a | act_2b | act_3)
- title: string (praegnanter Titel fuer diesen Beat)
- summary: string (150-300 Zeichen, konkreter Inhalt fuer diese Geschichte)
- tension: string (low | medium | high | peak)
- key_events: array of strings (2-4 konkrete Ereignisse)
"""


def _build_user_prompt(framework: FrameworkDefinition, context: ProjectContext) -> str:
    beats_overview = "\n".join(
        f"  {i + 1}. [{b.position:.2f}] {b.name}: {b.description}"
        for i, b in enumerate(framework.beats)
    )
    themes_str = ", ".join(context.themes) if context.themes else "nicht spezifiziert"
    return f"""\
Framework: {framework.name} ({len(framework.beats)} Beats)

Beats in Reihenfolge:
{beats_overview}

Projekt-Kontext:
- Titel: {context.title}
- Genre: {context.genre}
- Logline: {context.logline}
- Protagonist: {context.protagonist}
- Setting: {context.setting}
- Themen: {themes_str}
- Ton: {context.tone or "nicht spezifiziert"}
- Ausgabesprache: {context.language_code}

Erstelle jetzt das vollstaendige JSON-Array mit allen {len(framework.beats)} Beats.
Jeder Beat muss konkret auf diese spezifische Geschichte zugeschnitten sein.
"""


def _build_result(
    raw_response: str,
    framework_key: str,
    framework: FrameworkDefinition,
    context: ProjectContext,
    start_ms: int,
) -> OutlineResult:
    """Parse raw LLM response and build OutlineResult.

    Shared by sync and async paths.
    """
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
    """Build error OutlineResult."""
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
    Generates story outlines by calling an LLMRouter and parsing the response.

    Usage (sync):
        generator = OutlineGenerator(router=my_aifw_router)
        result = generator.generate("save_the_cat", context=ProjectContext(...))

    Usage (async):
        generator = OutlineGenerator(router=my_async_router)
        result = await generator.agenerate(framework_key="save_the_cat", context=ctx)
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
                GenerationStatus.VALIDATION_ERROR,
                framework_key,
                "",
                context.title,
                str(e),
                0,
                start_ms,
            )

        messages = [
            {"role": "system", "content": _SYSTEM_PROMPT},
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
                GenerationStatus.LLM_ERROR,
                framework_key,
                framework.name,
                context.title,
                f"LLM timeout: {e}",
                len(framework.beats),
                start_ms,
            )
        except LLMRouterError as e:
            logger.error("LLM error: %s", e)
            return _error_result(
                GenerationStatus.LLM_ERROR,
                framework_key,
                framework.name,
                context.title,
                str(e),
                len(framework.beats),
                start_ms,
            )

        return _build_result(raw_response, framework_key, framework, context, start_ms)

    async def agenerate(
        self,
        framework_key: str,
        context: ProjectContext,
        quality: LLMQuality = LLMQuality.STANDARD,
        priority: str = "balanced",
    ) -> OutlineResult:
        """Async variant of generate(). Requires router with acompletion()."""
        if not isinstance(self._router, AsyncLLMRouter):
            raise TypeError(
                "Async agenerate() requires a router implementing AsyncLLMRouter.acompletion()"
            )

        start_ms = int(time.time() * 1000)

        try:
            framework = get_framework(framework_key)
        except KeyError as e:
            return _error_result(
                GenerationStatus.VALIDATION_ERROR,
                framework_key,
                "",
                context.title,
                str(e),
                0,
                start_ms,
            )

        messages = [
            {"role": "system", "content": _SYSTEM_PROMPT},
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
                GenerationStatus.LLM_ERROR,
                framework_key,
                framework.name,
                context.title,
                f"LLM timeout: {e}",
                len(framework.beats),
                start_ms,
            )
        except LLMRouterError as e:
            logger.error("LLM error (async): %s", e)
            return _error_result(
                GenerationStatus.LLM_ERROR,
                framework_key,
                framework.name,
                context.title,
                str(e),
                len(framework.beats),
                start_ms,
            )

        return _build_result(raw_response, framework_key, framework, context, start_ms)
