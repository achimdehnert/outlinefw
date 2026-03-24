"""Tests for async OutlineGenerator.agenerate()."""

from __future__ import annotations

import pytest

from outlinefw.generator import OutlineGenerator
from outlinefw.schemas import GenerationStatus, ProjectContext
from tests.conftest import AsyncGoodRouter, EmptyRouter, ErrorRouter, TimeoutRouter


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


@pytest.mark.asyncio
async def test_async_successful_generation(
    sample_context: ProjectContext,
) -> None:
    gen = OutlineGenerator(router=AsyncGoodRouter("three_act"))
    result = await gen.agenerate("three_act", sample_context)
    assert result.status == GenerationStatus.SUCCESS
    assert len(result.nodes) == 7


@pytest.mark.asyncio
async def test_async_llm_error(
    sample_context: ProjectContext,
) -> None:
    gen = OutlineGenerator(router=ErrorRouter())
    result = await gen.agenerate("three_act", sample_context)
    assert result.status == GenerationStatus.LLM_ERROR


@pytest.mark.asyncio
async def test_async_timeout(
    sample_context: ProjectContext,
) -> None:
    gen = OutlineGenerator(router=TimeoutRouter())
    result = await gen.agenerate("three_act", sample_context)
    assert result.status == GenerationStatus.LLM_ERROR
    assert "timeout" in result.error_message.lower()


@pytest.mark.asyncio
async def test_async_empty_response(
    sample_context: ProjectContext,
) -> None:
    gen = OutlineGenerator(router=EmptyRouter())
    result = await gen.agenerate("three_act", sample_context)
    assert result.status == GenerationStatus.PARSE_ERROR


@pytest.mark.asyncio
async def test_async_unknown_framework(
    sample_context: ProjectContext,
) -> None:
    gen = OutlineGenerator(router=AsyncGoodRouter())
    result = await gen.agenerate("nonexistent", sample_context)
    assert result.status == GenerationStatus.VALIDATION_ERROR


@pytest.mark.asyncio
async def test_async_result_has_timing(
    sample_context: ProjectContext,
) -> None:
    gen = OutlineGenerator(router=AsyncGoodRouter())
    result = await gen.agenerate("three_act", sample_context)
    assert result.generation_time_ms is not None
    assert result.generation_time_ms >= 0
