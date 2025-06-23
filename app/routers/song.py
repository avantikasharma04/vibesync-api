from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.song import Song
from app.schemas.song import SongCreate, SongOut

router = APIRouter(prefix="/songs", tags=["Songs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SongOut)
def create_song(song: SongCreate, db: Session = Depends(get_db)):
    new_song = Song(**song.dict())
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song

@router.get("/", response_model=list[SongOut])
def get_all_songs(db: Session = Depends(get_db)):
    return db.query(Song).all()

@router.get("/{song_id}", response_model=SongOut)
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@router.put("/{song_id}", response_model=SongOut)
def update_song(song_id: int, updated_song: SongCreate, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    for key, value in updated_song.dict().items():
        setattr(song, key, value)
    db.commit()
    db.refresh(song)
    return song

@router.delete("/{song_id}")
def delete_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    db.delete(song)
    db.commit()
    return {"message": "Song deleted successfully"}
