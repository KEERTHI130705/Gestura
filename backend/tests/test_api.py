import asyncio
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        resp = await ac.get('/health')
        assert resp.status_code == 200
        assert resp.json()['status'] == 'ok'


@pytest.mark.asyncio
async def test_mode_switch():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        r1 = await ac.get('/mode')
        assert r1.status_code == 200
        cur = r1.json()['mode']
        for m in ['letters', 'words', 'sentences']:
            r2 = await ac.post(f'/mode/{m}')
            assert r2.status_code == 200
            assert r2.json()['ok'] is True
        r3 = await ac.post('/mode/invalid')
        assert r3.status_code == 200
        assert r3.json()['ok'] is False
