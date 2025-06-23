import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_song_api():
    response = client.post("/songs/", json={
        "title": "API Song",
        "artist": "API Artist"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "API Song"
    assert data["artist"] == "API Artist"

def test_get_all_songs_api():
    response = client.get("/songs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_song_api_not_found():
    response = client.get("/songs/99999")
    assert response.status_code == 404
