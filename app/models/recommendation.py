from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Recommendation(Base):
    __tablename__ = 'recommendations'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # book/movie
    title = Column(String)
    description = Column(String)
    song_id = Column(Integer, ForeignKey("songs.id"))
