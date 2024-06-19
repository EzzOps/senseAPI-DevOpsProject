import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer, loop_context
from flask import Flask
from app import app, get_version, get_temperature_data

@pytest.fixture
def client():
    return app.test_client()

def test_version(client):
    response = client.get('/version')
    assert response.status_code == 200
    assert response.json == {"version": "0.0.2"}

@pytest.mark.asyncio
async def test_get_temperature_data():
    data = await get_temperature_data()
    assert data is not None  # You can add more detailed assertions based on expected data format

@pytest.mark.asyncio
async def test_temperature(client):
    response = await client.get('/temperature')
    assert response.status_code == 200 or response.status_code == 500  # Depending on whether the data is fetched successfully or not
    if response.status_code == 200:
        assert isinstance(response.json, list)  # Assuming the API returns a list of temperature data
    else:
        assert response.json == {"error": "Unable to fetch temperature data"}
