import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.recommendation import Recommendation
from app.models.song import Song
from app.routers.recommendation import (
    create_recommendation,
    get_recommendations,
    delete_recommendation
)
from app.schemas.recommendation import RecommendationCreate
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

def test_create_recommendation_integration(db):
    song = Song(title="Trigger Song", artist="Artist X")
    db.add(song)
    db.commit()
    db.refresh(song)

    rec_data = RecommendationCreate(
        type="book",
        title="Deep Work",
        description="A book about focus",
        song_id=song.id
    )
    result = create_recommendation(rec=rec_data, db=db)

    assert result.title == "Deep Work"
    assert result.song_id == song.id

def test_get_recommendations_integration(db):
    song = Song(title="Explore Song", artist="Artist Y")
    db.add(song)
    db.commit()
    db.refresh(song)

    rec = Recommendation(
        type="movie",
        title="Soul",
        description="A Pixar movie",
        song_id=song.id
    )
    db.add(rec)
    db.commit()

    results = get_recommendations(song_id=song.id, db=db)
    assert len(results) == 1
    assert results[0].title == "Soul"

def test_delete_recommendation_integration(db):
    song = Song(title="Delete Me", artist="Z")
    db.add(song)
    db.commit()
    db.refresh(song)

    rec = Recommendation(
        type="book",
        title="Atomic Habits",
        description="Tiny changes, big results",
        song_id=song.id
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    response = delete_recommendation(rec_id=rec.id, db=db)
    assert response["message"] == "Deleted successfully"
