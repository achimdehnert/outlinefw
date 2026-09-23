"""
outlinefw/src/outlinefw/__init__.py

Public API for iil-outlinefw.

Stable API (semantic versioning: breaking changes -> MAJOR bump):
  Schemas:    ProjectContext, OutlineNode, OutlineResult, ParseResult
  Generator:  OutlineGenerator, LLMRouter, LLMRouterError, LLMRouterTimeout
  Prompts:    default_user_prompt, default_system_prompt (ADR-204, since 0.4.0)
  Parser:     parse_nodes
  Frameworks: FRAMEWORKS, get_framework, list_frameworks, register_framework
"""

from importlib.metadata import PackageNotFoundError, version

from outlinefw.export import to_dict, to_json, to_markdown
from outlinefw.frameworks import (
    FRAMEWORKS,
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
    default_system_prompt,
    default_user_prompt,
)
from outlinefw.parser import parse_nodes
from outlinefw.schemas import (
    ActPhase,
    BeatDefinition,
    FrameworkDefinition,
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

try:
    __version__ = version("iil-outlinefw")
except PackageNotFoundError:  # running from source without an install
    __version__ = "0.0.0+unknown"

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
    "default_system_prompt",
    "default_user_prompt",
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
