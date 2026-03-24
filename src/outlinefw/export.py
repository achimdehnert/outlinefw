"""
outlinefw/src/outlinefw/export.py

Export functions for OutlineResult and OutlineNode.
Supports Markdown, JSON, and dict export formats.
"""

from __future__ import annotations

import json
from typing import Any

from outlinefw.schemas import OutlineNode, OutlineResult


def to_markdown(result: OutlineResult, include_metadata: bool = True) -> str:
    """Export an OutlineResult as formatted Markdown.

    Args:
        result: The outline to export.
        include_metadata: Include header with framework info and stats.
    """
    lines: list[str] = []

    if include_metadata:
        lines.append(f"# {result.project_title}")
        lines.append("")
        lines.append(f"**Framework:** {result.framework_name} ({result.framework_key})")
        lines.append(
            f"**Status:** {result.status.value} "
            f"| **Beats:** {result.generated_beats}/{result.total_beats}"
        )
        if result.generation_time_ms is not None:
            lines.append(f"**Generation Time:** {result.generation_time_ms}ms")
        lines.append("")
        lines.append("---")
        lines.append("")

    for i, node in enumerate(result.nodes, 1):
        lines.append(_node_to_markdown(node, i))
        lines.append("")

    return "\n".join(lines)


def _node_to_markdown(node: OutlineNode, number: int) -> str:
    """Format a single OutlineNode as Markdown."""
    lines = [
        f"## {number}. {node.title}",
        "",
        f"**Beat:** {node.beat_name} | "
        f"**Position:** {node.position:.2f} | "
        f"**Act:** {node.act.value} | "
        f"**Tension:** {node.tension.value}",
        "",
        node.summary,
    ]

    if node.key_events:
        lines.append("")
        lines.append("**Key Events:**")
        for event in node.key_events:
            lines.append(f"- {event}")

    if node.character_arcs:
        lines.append("")
        lines.append("**Character Arcs:**")
        for char, arc in node.character_arcs.items():
            lines.append(f"- **{char}:** {arc}")

    return "\n".join(lines)


def to_json(
    result: OutlineResult,
    indent: int = 2,
    include_raw: bool = False,
) -> str:
    """Export an OutlineResult as JSON string.

    Args:
        result: The outline to export.
        indent: JSON indentation level.
        include_raw: Include raw LLM response in output.
    """
    data = to_dict(result, include_raw=include_raw)
    return json.dumps(data, indent=indent, ensure_ascii=False)


def to_dict(
    result: OutlineResult,
    include_raw: bool = False,
) -> dict[str, Any]:
    """Export an OutlineResult as a plain dictionary.

    Args:
        result: The outline to export.
        include_raw: Include raw LLM response in output.
    """
    data: dict[str, Any] = {
        "project_title": result.project_title,
        "framework_key": result.framework_key,
        "framework_name": result.framework_name,
        "status": result.status.value,
        "total_beats": result.total_beats,
        "generated_beats": result.generated_beats,
        "completion_ratio": round(result.completion_ratio, 2),
        "nodes": [_node_to_dict(n) for n in result.nodes],
    }

    if result.generation_time_ms is not None:
        data["generation_time_ms"] = result.generation_time_ms

    if result.error_message:
        data["error_message"] = result.error_message

    if include_raw and result.raw_llm_response:
        data["raw_llm_response"] = result.raw_llm_response

    return data


def _node_to_dict(node: OutlineNode) -> dict[str, Any]:
    """Convert an OutlineNode to a plain dict."""
    return {
        "beat_name": node.beat_name,
        "position": node.position,
        "act": node.act.value,
        "title": node.title,
        "summary": node.summary,
        "tension": node.tension.value,
        "scene_count": node.scene_count,
        "key_events": node.key_events,
        "character_arcs": node.character_arcs,
    }
