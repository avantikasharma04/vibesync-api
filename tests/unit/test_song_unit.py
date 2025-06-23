import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from unittest.mock import MagicMock
from fastapi import HTTPException
from app.routers.song import create_song, get_song
from app.schemas.song import SongCreate
from app.models.song import Song

def test_create_song_unit():
    db = MagicMock()
    song_data = SongCreate(title="Test Title", artist="Test Artist")
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    result = create_song(song=song_data, db=db)

    assert result.title == "Test Title"
    assert result.artist == "Test Artist"

def test_get_song_unit_found():
    db = MagicMock()
    song = Song(id=1, title="Existing Song", artist="Artist")
    db.query().filter().first.return_value = song

    result = get_song(song_id=1, db=db)
    assert result.title == "Existing Song"

def test_get_song_unit_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    try:
        get_song(song_id=1, db=db)
        assert False, "Expected HTTPException"
    except HTTPException as e:
        assert e.status_code == 404
