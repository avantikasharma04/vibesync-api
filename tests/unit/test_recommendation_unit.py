import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from unittest.mock import MagicMock
from fastapi import HTTPException
from app.routers.recommendation import create_recommendation, get_recommendations, delete_recommendation
from app.schemas.recommendation import RecommendationCreate
from app.models.recommendation import Recommendation

def test_create_recommendation_unit():
    db = MagicMock()
    rec_data = RecommendationCreate(
        type="book",
        title="Test Book",
        description="Great book!",
        song_id=1
    )
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    result = create_recommendation(rec=rec_data, db=db)

    assert result.title == "Test Book"
    assert result.description == "Great book!"

def test_get_recommendations_unit():
    db = MagicMock()
    recommendation = Recommendation(id=1, type="movie", title="Inception", description="Mind-blowing", song_id=1)
    db.query().filter().all.return_value = [recommendation]

    result = get_recommendations(song_id=1, db=db)
    assert len(result) == 1
    assert result[0].title == "Inception"

def test_delete_recommendation_unit():
    db = MagicMock()
    recommendation = Recommendation(id=1, type="movie", title="Inception", description="Mind-blowing", song_id=1)
    db.query().filter().first.return_value = recommendation
    db.delete = MagicMock()
    db.commit = MagicMock()

    response = delete_recommendation(rec_id=1, db=db)
    assert response["message"] == "Deleted successfully"

def test_delete_recommendation_unit_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    try:
        delete_recommendation(rec_id=1, db=db)
        assert False, "Expected HTTPException"
    except HTTPException as e:
        assert e.status_code == 404
