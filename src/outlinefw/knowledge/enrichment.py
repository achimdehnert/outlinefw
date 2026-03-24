"""
outlinefw.knowledge.enrichment — Feed Wiki research into OutlineGenerator.

Bridge between Outline Wiki knowledge and story outline generation.
"""

from __future__ import annotations

from typing import Any

from outlinefw.schemas import ProjectContext


def enrich_context(
    context: ProjectContext,
    wiki_documents: list[dict[str, Any]],
    max_chars: int = 4000,
) -> ProjectContext:
    """Enrich a ProjectContext with knowledge from Wiki documents.

    Appends relevant Wiki content to additional_notes so the
    OutlineGenerator's LLM prompt includes this research context.

    Args:
        context: Original project context.
        wiki_documents: List of dicts with 'title' and 'text' keys
            (as returned by OutlineWikiClient.search()).
        max_chars: Maximum characters to append (to stay within
            LLM context limits).

    Returns:
        New ProjectContext with enriched additional_notes.
    """
    if not wiki_documents:
        return context

    research_parts: list[str] = []
    total_chars = 0

    for doc in wiki_documents:
        title = doc.get("title", "Untitled")
        text = doc.get("text", doc.get("context", ""))
        if not text:
            continue

        snippet = f"### {title}\n{text}"
        if total_chars + len(snippet) > max_chars:
            remaining = max_chars - total_chars
            if remaining > 100:
                snippet = snippet[:remaining] + "..."
                research_parts.append(snippet)
            break

        research_parts.append(snippet)
        total_chars += len(snippet)

    if not research_parts:
        return context

    research_block = "--- Wiki Research ---\n" + "\n\n".join(research_parts)

    existing = context.additional_notes
    separator = "\n\n" if existing else ""
    new_notes = f"{existing}{separator}{research_block}"

    # Truncate to field max_length (2000)
    if len(new_notes) > 2000:
        new_notes = new_notes[:1997] + "..."

    return context.model_copy(update={"additional_notes": new_notes})
