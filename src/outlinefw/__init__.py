"""
outlinefw -- Story Outline Framework
=====================================

Pure-Python, framework-agnostic outline generation.
No Django, no DB -- only Pydantic schemas + LLM generation logic.

Usage:
    from outlinefw import OutlineGenerator, FRAMEWORKS
    from outlinefw.schemas import OutlineNode, OutlineResult
    from outlinefw.django_adapter import save_outline_to_db  # only with Django
"""

from .frameworks import FRAMEWORKS, get_framework, list_frameworks
from .generator import OutlineGenerator
from .parser import parse_nodes
from .schemas import OutlineNode, OutlineResult, ProjectContext

__all__ = [
    "FRAMEWORKS",
    "get_framework",
    "list_frameworks",
    "OutlineGenerator",
    "parse_nodes",
    "OutlineNode",
    "OutlineResult",
    "ProjectContext",
]
