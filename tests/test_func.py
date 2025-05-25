import uuid
import re
import pytest

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_load():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/load", data={"count": 10})
    assert response.status_code in (200, 302)
    assert "set-cookie" in response.headers
    assert response.headers.get("location") == '/'

@pytest.mark.asyncio
async def test_index():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/load", data={"count": 10})
        assert response.status_code in (200, 302)
        response = await client.get("/")
        assert response.status_code == 200
        assert "Пользователи" in response.text
        assert "Случайный пользователь" in response.text
        assert "Пол" in response.text

@pytest.mark.asyncio
async def test_random_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/load", data={"count": 10})
        assert response.status_code in (200, 302)
        response = await client.get("/random")
        assert response.status_code == 200
        assert "Информация" in response.text

@pytest.mark.asyncio
async def test_user_detail():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/load", data={"count": 10})
        assert response.status_code in (200, 302)
        index_response = await client.get("/")
        assert index_response.status_code == 200

        match = re.search(r'href="/user/([0-9a-fA-F-]{36})"', index_response.text)
        user_id = match.group(1)

        detail_response = await client.get(f"/user/{user_id}")
        assert detail_response.status_code == 200
        assert "Информация" in detail_response.text

@pytest.mark.asyncio
async def test_user_detail_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/user/{uuid.uuid4()}")
    assert response.status_code in (200, 404)