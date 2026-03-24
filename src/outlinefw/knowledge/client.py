"""
outlinefw.knowledge.client — Async HTTP client for Outline Wiki REST API.

Extracted from outline-mcp (packages/outline-mcp/outline_mcp/client.py)
and generalized for use in any Python project.

Requires: pip install iil-outlinefw[knowledge]
"""

from __future__ import annotations

import logging
from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from outlinefw.knowledge.settings import KnowledgeSettings

logger = logging.getLogger(__name__)

RETRY_POLICY = retry(
    retry=retry_if_exception_type((httpx.ConnectError, httpx.ReadTimeout)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
)


class OutlineWikiClient:
    """Async HTTP client for the Outline Wiki REST API.

    Usage::

        async with OutlineWikiClient() as client:
            results = await client.search("Django deployment")
            doc = await client.get_document(results[0]["id"])

    Or with explicit settings::

        settings = KnowledgeSettings(
            url="https://knowledge.iil.pet",
            api_token="ol_api_...",
        )
        client = OutlineWikiClient(settings=settings)
    """

    def __init__(
        self,
        settings: KnowledgeSettings | None = None,
    ) -> None:
        self._settings = settings or KnowledgeSettings()
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> OutlineWikiClient:
        self._client = self._build_client()
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    def _build_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=f"{self._settings.url}/api/",
            headers={
                "Authorization": f"Bearer {self._settings.api_token}",
                "Content-Type": "application/json",
            },
            timeout=self._settings.timeout,
        )

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = self._build_client()
        return self._client

    @RETRY_POLICY
    async def search(
        self,
        query: str,
        collection_id: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Full-text search across documents.

        Returns list of document dicts with id, title, text snippet.
        """
        payload: dict[str, Any] = {
            "query": query,
            "limit": limit or self._settings.default_limit,
            "offset": offset,
        }
        if collection_id:
            payload["collectionId"] = collection_id

        resp = await self._get_client().post("documents.search", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return [
            {
                "id": item["document"]["id"],
                "title": item["document"]["title"],
                "text": item["document"].get("text", ""),
                "context": item.get("context", ""),
                "ranking": item.get("ranking", 0),
            }
            for item in data.get("data", [])
        ]

    @RETRY_POLICY
    async def get_document(self, document_id: str) -> dict[str, Any]:
        """Get full document content by ID."""
        resp = await self._get_client().post("documents.info", json={"id": document_id})
        resp.raise_for_status()
        doc = resp.json().get("data", {})
        return {
            "id": doc.get("id", ""),
            "title": doc.get("title", ""),
            "text": doc.get("text", ""),
            "collection_id": doc.get("collectionId", ""),
            "created_at": doc.get("createdAt", ""),
            "updated_at": doc.get("updatedAt", ""),
        }

    @RETRY_POLICY
    async def create_document(
        self,
        title: str,
        text: str,
        collection_id: str,
        publish: bool = True,
    ) -> dict[str, Any]:
        """Create a new document in a collection."""
        resp = await self._get_client().post(
            "documents.create",
            json={
                "title": title,
                "text": text,
                "collectionId": collection_id,
                "publish": publish,
            },
        )
        resp.raise_for_status()
        doc = resp.json().get("data", {})
        return {"id": doc.get("id", ""), "url": doc.get("url", "")}

    @RETRY_POLICY
    async def update_document(
        self,
        document_id: str,
        title: str | None = None,
        text: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing document."""
        payload: dict[str, Any] = {"id": document_id}
        if title is not None:
            payload["title"] = title
        if text is not None:
            payload["text"] = text

        resp = await self._get_client().post("documents.update", json=payload)
        resp.raise_for_status()
        return resp.json().get("data", {})

    @RETRY_POLICY
    async def delete_document(self, document_id: str) -> dict[str, Any]:
        """Delete a document (moves to trash)."""
        resp = await self._get_client().post("documents.delete", json={"id": document_id})
        resp.raise_for_status()
        return resp.json()

    @RETRY_POLICY
    async def list_collections(self) -> list[dict[str, Any]]:
        """List all collections."""
        resp = await self._get_client().post("collections.list", json={})
        resp.raise_for_status()
        return [
            {
                "id": col.get("id", ""),
                "name": col.get("name", ""),
                "description": col.get("description", ""),
            }
            for col in resp.json().get("data", [])
        ]

    async def close(self) -> None:
        """Explicitly close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
