"""
outlinefw.django_adapter -- Optional Django bridge.

Nur diese Datei hat Django-Abhaengigkeiten.
Alle anderen Module sind pure Python.

Host-App muss project_context_from_db und save_outline_to_db
mit eigenen Implementierungen ueberschreiben.
"""
from __future__ import annotations

import logging

from .schemas import OutlineNode, ProjectContext

logger = logging.getLogger(__name__)


def project_context_from_db(project_id: str) -> ProjectContext:
    """Stub -- muss von der Host-App implementiert werden."""
    raise NotImplementedError(
        "project_context_from_db muss von der Host-App implementiert werden. "
        "Beispiel writing-hub: from apps.projects.models import BookProject"
    )


def save_outline_to_db(
    project_id: str,
    nodes: list[OutlineNode],
    name: str = "KI-generiert",
    framework: str = "",
    user=None,
) -> str | None:
    """Stub -- muss von der Host-App implementiert werden."""
    raise NotImplementedError(
        "save_outline_to_db muss von der Host-App implementiert werden."
    )
