"""
outlinefw/src/outlinefw/__init__.py

Public API for iil-outlinefw.

Stable API (semantic versioning: breaking changes -> MAJOR bump):
  Schemas:    ProjectContext, OutlineNode, OutlineResult, ParseResult
  Generator:  OutlineGenerator, LLMRouter, LLMRouterError, LLMRouterTimeout
  Parser:     parse_nodes
  Frameworks: FRAMEWORKS, get_framework, list_frameworks
"""

from outlinefw.export import to_dict, to_json, to_markdown
from outlinefw.frameworks import (
    FRAMEWORKS,
    FrameworkDefinition,
    get_framework,
    list_frameworks,
    register_framework,
    unregister_framework,
)
from outlinefw.generator import (
    AsyncLLMRouter,
    LLMRouter,
    LLMRouterError,
    LLMRouterTimeout,
    OutlineGenerator,
)
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

__version__ = "0.2.0"

__all__ = [
    # Framework Registry
    "FRAMEWORKS",
    # Enums
    "ActPhase",
    # LLM Router Protocols
    "AsyncLLMRouter",
    "BeatDefinition",
    "FrameworkDefinition",
    "GenerationStatus",
    "LLMQuality",
    "LLMRouter",
    "LLMRouterError",
    "LLMRouterTimeout",
    # Core Generation
    "OutlineGenerationError",
    "OutlineGenerator",
    "OutlineNode",
    "OutlineResult",
    "ParseResult",
    "ParseStatus",
    "ProjectContext",
    "TensionLevel",
    # Version
    "__version__",
    "get_framework",
    "list_frameworks",
    "parse_nodes",
    "register_framework",
    # Export
    "to_dict",
    "to_json",
    "to_markdown",
    "unregister_framework",
]
