"""
outlinefw.knowledge — Outline Wiki integration layer.

Optional extra: pip install iil-outlinefw[knowledge]

Provides:
- OutlineWikiClient: async HTTP client for Outline Wiki REST API
- KnowledgeSettings: pydantic-settings for Wiki configuration
- enrich_context: feed Wiki research into OutlineGenerator
"""

from outlinefw.knowledge.client import OutlineWikiClient
from outlinefw.knowledge.enrichment import enrich_context
from outlinefw.knowledge.settings import KnowledgeSettings

__all__ = [
    "KnowledgeSettings",
    "OutlineWikiClient",
    "enrich_context",
]
