import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.song import Song
from app.routers.song import create_song, get_song
from app.schemas.song import SongCreate
from fastapi import HTTPException

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_song_integration(db):
    song_data = SongCreate(title="Real Song", artist="Real Artist")
    result = create_song(song=song_data, db=db)

    assert result.title == "Real Song"
    assert result.artist == "Real Artist"

def test_get_song_integration(db):
    song = Song(title="Fetch Me", artist="Artist X")
    db.add(song)
    db.commit()
    db.refresh(song)

    result = get_song(song_id=song.id, db=db)
    assert result.title == "Fetch Me"
