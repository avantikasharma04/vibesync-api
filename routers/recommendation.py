from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.recommendation import Recommendation
from schemas.recommendation import RecommendationCreate, RecommendationOut

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RecommendationOut)
def create_recommendation(rec: RecommendationCreate, db: Session = Depends(get_db)):
    new_rec = Recommendation(**rec.dict())
    db.add(new_rec)
    db.commit()
    db.refresh(new_rec)
    return new_rec

@router.get("/song/{song_id}", response_model=list[RecommendationOut])
def get_recommendations(song_id: int, db: Session = Depends(get_db)):
    return db.query(Recommendation).filter(Recommendation.song_id == song_id).all()

@router.delete("/{rec_id}")
def delete_recommendation(rec_id: int, db: Session = Depends(get_db)):
    rec = db.query(Recommendation).filter(Recommendation.id == rec_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    db.delete(rec)
    db.commit()
    return {"message": "Deleted successfully"}

@router.put("/{rec_id}", response_model=RecommendationOut)
def update_recommendation(rec_id: int, updated: RecommendationCreate, db: Session = Depends(get_db)):
    rec = db.query(Recommendation).filter(Recommendation.id == rec_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    for key, value in updated.dict().items():
        setattr(rec, key, value)
    db.commit()
    db.refresh(rec)
    return rec
