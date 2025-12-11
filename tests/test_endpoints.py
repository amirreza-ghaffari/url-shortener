"""Tests for URL shortener API endpoints."""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest_asyncio.fixture(name="client")
async def client_fixture():
    """Create an async test client."""
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_short_url(client: AsyncClient):
    """Test creating a short URL."""
    response = await client.post(
        "/shorten",
        json={"long_url": "https://www.example.com/test"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert data["original_url"] == "https://www.example.com/test"


@pytest.mark.asyncio
async def test_redirect_short_url(client: AsyncClient):
    """Test redirecting to original URL."""

    create_response = await client.post(
        "/shorten",
        json={"long_url": "https://www.example.com/test"}
    )
    short_code = create_response.json()["short_code"]


    response = await client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://www.example.com/test"


@pytest.mark.asyncio
async def test_get_url_stats(client: AsyncClient):
    """Test getting URL statistics."""

    create_response = await client.post(
        "/shorten",
        json={"long_url": "https://www.example.com/stats-test"}
    )
    short_code = create_response.json()["short_code"]

    response = await client.get(f"/stats/{short_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["short_code"] == short_code
    assert data["original_url"] == "https://www.example.com/stats-test"
    assert data["visit_count"] == 0  # No visits yet


@pytest.mark.asyncio
async def test_duplicate_url(client: AsyncClient):
    """Test that same URL returns same short code."""
    url = "https://www.example.com/duplicate-test"

    response1 = await client.post("/shorten", json={"long_url": url})
    short_code1 = response1.json()["short_code"]

    response2 = await client.post("/shorten", json={"long_url": url})
    short_code2 = response2.json()["short_code"]

    assert short_code1 == short_code2


@pytest.mark.asyncio
async def test_visit_counter_increments(client: AsyncClient):
    """Test that visit counter increments on each redirect."""

    create_response = await client.post(
        "/shorten",
        json={"long_url": "https://www.example.com/counter-test"}
    )
    short_code = create_response.json()["short_code"]

    await client.get(f"/{short_code}", follow_redirects=False)

    stats_response = await client.get(f"/stats/{short_code}")
    old_visit_count = stats_response.json()["visit_count"]

    await client.get(f"/{short_code}", follow_redirects=False)

    stats_response = await client.get(f"/stats/{short_code}")

    assert stats_response.json()["visit_count"] == old_visit_count + 1


@pytest.mark.asyncio
async def test_nonexistent_short_code(client: AsyncClient):
    """Test accessing a non-existent short code."""
    response = await client.get("/nonexistent123")
    assert response.status_code == 404

