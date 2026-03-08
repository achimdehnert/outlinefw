"""
outlinefw/src/outlinefw/__init__.py

Public API for iil-outlinefw.

Stable API (semantic versioning: breaking changes -> MAJOR bump):
  Schemas:    ProjectContext, OutlineNode, OutlineResult, ParseResult
  Generator:  OutlineGenerator, LLMRouter, LLMRouterError, LLMRouterTimeout
  Parser:     parse_nodes
  Frameworks: FRAMEWORKS, get_framework, list_frameworks
"""

from outlinefw.frameworks import FRAMEWORKS, FrameworkDefinition, get_framework, list_frameworks
from outlinefw.generator import LLMRouter, LLMRouterError, LLMRouterTimeout, OutlineGenerator
from outlinefw.parser import parse_nodes
from outlinefw.schemas import (
    ActPhase,
    BeatDefinition,
    GenerationStatus,
    LLMQuality,
    OutlineGenerationError,
    OutlineNode,
    OutlineResult,
    ParseResult,
    ParseStatus,
    ProjectContext,
    TensionLevel,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # Core Generation
    "OutlineGenerator",
    "LLMRouter",
    "LLMRouterError",
    "LLMRouterTimeout",
    "parse_nodes",
    # Schemas
    "ProjectContext",
    "OutlineNode",
    "OutlineResult",
    "ParseResult",
    "BeatDefinition",
    "FrameworkDefinition",
    "OutlineGenerationError",
    # Enums
    "ActPhase",
    "TensionLevel",
    "LLMQuality",
    "GenerationStatus",
    "ParseStatus",
    # Framework Registry
    "FRAMEWORKS",
    "get_framework",
    "list_frameworks",
]
