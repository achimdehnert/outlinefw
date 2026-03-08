# iil-outlinefw

Story Outline Framework for AI-assisted creative writing.

**Pure Python** — no Django, no DB dependency in the core.

Part of the `iil-` platform package family alongside `iil-aifw`, `iil-authoringfw`, `iil-promptfw`.

## Install

```bash
pip install iil-outlinefw
# or with LLM support:
pip install iil-outlinefw[aifw]
```

## Features

- **5 story frameworks**: Three-Act, Save the Cat, Hero's Journey, Five-Act, Dan Harmon Story Circle
- **Beat definitions** with act position (0.0–1.0), tension level, emotional arc
- **`OutlineGenerator`**: LLM-based outline generation via any `iil-aifw`-compatible router
- **`parse_nodes()`**: Robust JSON parser for LLM responses (handles fencing, `<think>` tags, leading text)
- **Pydantic schemas**: `OutlineNode`, `OutlineResult`, `ProjectContext`
- **Django adapter** in `outlinefw.django_adapter` (optional, no hard dependency)

## Quick Start

```python
from outlinefw import OutlineGenerator, FRAMEWORKS
from outlinefw.schemas import ProjectContext

gen = OutlineGenerator(my_llm_router)

ctx = ProjectContext(
    title="My Novel",
    genre="Thriller",
    description="A story about ...",
)

result = gen.generate(ctx, framework="save_the_cat", chapter_count=15)
for node in result.nodes:
    print(f"{node.order}. {node.title} [{node.beat}]")
```

## Frameworks

| Key | Name | Beats |
|-----|------|-------|
| `three_act` | Drei-Akt-Struktur | 7 |
| `save_the_cat` | Save the Cat | 15 |
| `heros_journey` | Heldenreise | 12 |
| `five_act` | Fuenf-Akt-Struktur | 5 |
| `dan_harmon` | Dan Harmon Story Circle | 8 |

## Architecture

```
src/outlinefw/
    __init__.py        # Public API
    schemas.py         # Pydantic: OutlineNode, OutlineResult, ProjectContext
    frameworks.py      # FRAMEWORKS dict + BeatDefinition TypedDicts
    generator.py       # OutlineGenerator (LLMRouter Protocol)
    parser.py          # parse_nodes() -- robust LLM JSON parser
    django_adapter.py  # Optional Django bridge (override in host app)
```

## Used By

- `writing-hub` — outline generation + standalone Outlines section
- `travel-beat` — scene-based story planning (migration planned)
- `bfagent` — advanced outline handlers (migration planned)

## Part of the iil- Platform

| Package | Purpose |
|---------|---------|
| `iil-aifw` | LLM routing (DB-driven) |
| `iil-promptfw` | Prompt templates (Jinja2) |
| `iil-authoringfw` | Authoring schemas (chapters, style) |
| `iil-outlinefw` | Story structure + outline generation |
| `iil-weltenfw` | WeltenHub REST client |
