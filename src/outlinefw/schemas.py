"""
outlinefw.schemas -- Pydantic models (pure Python, no Django)
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class OutlineNode(BaseModel):
    """Ein einzelner Beat/Kapitel in einer Outline."""
    order: int = 0
    title: str
    description: str = ""
    beat_type: str = "chapter"
    beat: str = ""
    act: str = ""
    notes: str = ""
    emotional_arc: str = ""
    tension_level: str = ""
    target_words: int = 0


class OutlineResult(BaseModel):
    """Ergebnis einer Outline-Generierung."""
    success: bool
    nodes: list[OutlineNode] = Field(default_factory=list)
    framework: str = "three_act"
    error: str = ""


class ProjectContext(BaseModel):
    """Projektkontext fuer LLM-Prompts (framework-agnostic)."""
    title: str = ""
    genre: str = ""
    description: str = ""
    premise: str = ""
    logline: str = ""
    themes: str = ""
    target_audience: str = ""
    target_word_count: int = 0
    characters: list[dict] = Field(default_factory=list)
    worlds: list[dict] = Field(default_factory=list)

    def to_prompt_block(self) -> str:
        parts = []
        if self.title:
            parts.append(f"**Titel:** {self.title}")
        if self.genre:
            parts.append(f"**Genre:** {self.genre}")
        if self.description:
            parts.append(f"**Beschreibung:** {self.description}")
        if self.premise:
            parts.append(f"**Premise:** {self.premise}")
        if self.logline:
            parts.append(f"**Logline:** {self.logline}")
        if self.themes:
            parts.append(f"**Themen:** {self.themes}")
        if self.target_audience:
            parts.append(f"**Zielgruppe:** {self.target_audience}")
        if self.target_word_count:
            parts.append(f"**Ziel-Woerter:** {self.target_word_count:,}")
        if self.characters:
            lines = ["**Charaktere:**"]
            for c in self.characters[:5]:
                lines.append(f"- {c.get('name','?')} ({c.get('role','supporting')}): {c.get('description','')[:100]}")
            parts.append("\n".join(lines))
        if self.worlds:
            lines = ["**Welten/Settings:**"]
            for w in self.worlds[:3]:
                lines.append(f"- {w.get('name','?')}: {w.get('description','')[:100]}")
            parts.append("\n".join(lines))
        return "\n\n".join(parts) if parts else "(kein Kontext)"
