"""Tests for outlinefw.knowledge module (Wiki client + enrichment)."""

from __future__ import annotations

import httpx
import pytest
import respx

from outlinefw.knowledge.client import OutlineWikiClient
from outlinefw.knowledge.enrichment import enrich_context
from outlinefw.knowledge.settings import KnowledgeSettings
from outlinefw.schemas import ProjectContext

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------


class TestKnowledgeSettings:
    def test_defaults(self) -> None:
        s = KnowledgeSettings(api_token="test")
        assert s.url == "https://knowledge.iil.pet"
        assert s.default_limit == 10
        assert s.timeout == 30

    def test_custom_values(self) -> None:
        s = KnowledgeSettings(
            url="https://wiki.example.com",
            api_token="tok",
            default_limit=5,
            timeout=60,
        )
        assert s.url == "https://wiki.example.com"
        assert s.default_limit == 5


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


@pytest.fixture
def wiki_settings() -> KnowledgeSettings:
    return KnowledgeSettings(
        url="https://wiki.test",
        api_token="test-token",
    )


@pytest.fixture
def wiki_client(wiki_settings: KnowledgeSettings) -> OutlineWikiClient:
    return OutlineWikiClient(settings=wiki_settings)


class TestOutlineWikiClient:
    @respx.mock
    @pytest.mark.asyncio
    async def test_search(self, wiki_client: OutlineWikiClient) -> None:
        respx.post("https://wiki.test/api/documents.search").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "document": {
                                "id": "doc-1",
                                "title": "Test Doc",
                                "text": "Content here",
                            },
                            "context": "...snippet...",
                            "ranking": 0.95,
                        }
                    ]
                },
            )
        )
        results = await wiki_client.search("test query")
        assert len(results) == 1
        assert results[0]["id"] == "doc-1"
        assert results[0]["title"] == "Test Doc"

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_document(self, wiki_client: OutlineWikiClient) -> None:
        respx.post("https://wiki.test/api/documents.info").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "id": "doc-1",
                        "title": "Full Doc",
                        "text": "Full content",
                        "collectionId": "col-1",
                        "createdAt": "2026-01-01",
                        "updatedAt": "2026-03-01",
                    }
                },
            )
        )
        doc = await wiki_client.get_document("doc-1")
        assert doc["title"] == "Full Doc"
        assert doc["collection_id"] == "col-1"

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_document(self, wiki_client: OutlineWikiClient) -> None:
        respx.post("https://wiki.test/api/documents.create").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "id": "new-doc",
                        "url": "/doc/new-doc-abc",
                    }
                },
            )
        )
        result = await wiki_client.create_document(
            title="New", text="Content", collection_id="col-1"
        )
        assert result["id"] == "new-doc"

    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_document(self, wiki_client: OutlineWikiClient) -> None:
        respx.post("https://wiki.test/api/documents.delete").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        result = await wiki_client.delete_document("doc-1")
        assert result["success"] is True

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_collections(self, wiki_client: OutlineWikiClient) -> None:
        respx.post("https://wiki.test/api/collections.list").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "col-1",
                            "name": "Runbooks",
                            "description": "How-to guides",
                        },
                        {
                            "id": "col-2",
                            "name": "Concepts",
                            "description": "",
                        },
                    ]
                },
            )
        )
        cols = await wiki_client.list_collections()
        assert len(cols) == 2
        assert cols[0]["name"] == "Runbooks"

    @respx.mock
    @pytest.mark.asyncio
    async def test_search_with_collection_filter(self, wiki_client: OutlineWikiClient) -> None:
        route = respx.post("https://wiki.test/api/documents.search").mock(
            return_value=httpx.Response(200, json={"data": []})
        )
        await wiki_client.search("q", collection_id="col-1")
        body = route.calls[0].request.content
        assert b"collectionId" in body

    @respx.mock
    @pytest.mark.asyncio
    async def test_context_manager(self, wiki_settings: KnowledgeSettings) -> None:
        respx.post("https://wiki.test/api/collections.list").mock(
            return_value=httpx.Response(200, json={"data": []})
        )
        async with OutlineWikiClient(settings=wiki_settings) as client:
            cols = await client.list_collections()
            assert cols == []


# ---------------------------------------------------------------------------
# Enrichment
# ---------------------------------------------------------------------------


class TestEnrichContext:
    @pytest.fixture
    def base_context(self) -> ProjectContext:
        return ProjectContext(
            title="Test Story",
            genre="Fantasy",
            logline="A wizard discovers a hidden world beneath the city.",
            protagonist="Wizard Elara",
            setting="Modern Berlin",
            language_code="de",
        )

    def test_enriches_additional_notes(self, base_context: ProjectContext) -> None:
        docs = [
            {"title": "Berlin History", "text": "Berlin was founded in 1237."},
        ]
        enriched = enrich_context(base_context, docs)
        assert "Berlin History" in enriched.additional_notes
        assert "1237" in enriched.additional_notes

    def test_empty_docs_returns_original(self, base_context: ProjectContext) -> None:
        enriched = enrich_context(base_context, [])
        assert enriched.additional_notes == base_context.additional_notes

    def test_preserves_existing_notes(self) -> None:
        ctx = ProjectContext(
            title="X",
            genre="Y",
            logline="A story about something interesting.",
            protagonist="Hero",
            setting="Somewhere",
            additional_notes="Existing notes here.",
        )
        docs = [{"title": "Extra", "text": "Extra research content."}]
        enriched = enrich_context(ctx, docs)
        assert "Existing notes here." in enriched.additional_notes
        assert "Extra research" in enriched.additional_notes

    def test_respects_max_chars(self, base_context: ProjectContext) -> None:
        long_text = "A" * 5000
        docs = [{"title": "Long", "text": long_text}]
        enriched = enrich_context(base_context, docs, max_chars=200)
        assert len(enriched.additional_notes) <= 2000

    def test_truncates_to_field_limit(self, base_context: ProjectContext) -> None:
        docs = [{"title": f"Doc {i}", "text": "X" * 300} for i in range(20)]
        enriched = enrich_context(base_context, docs, max_chars=10000)
        assert len(enriched.additional_notes) <= 2000

    def test_does_not_mutate_original(self, base_context: ProjectContext) -> None:
        docs = [{"title": "T", "text": "Some research text."}]
        enriched = enrich_context(base_context, docs)
        assert base_context.additional_notes == ""
        assert enriched.additional_notes != ""

    def test_skips_empty_text_docs(self, base_context: ProjectContext) -> None:
        docs = [
            {"title": "Empty", "text": ""},
            {"title": "Real", "text": "Real content here."},
        ]
        enriched = enrich_context(base_context, docs)
        assert "Empty" not in enriched.additional_notes
        assert "Real content" in enriched.additional_notes
