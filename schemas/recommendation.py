from pydantic import BaseModel

class RecommendationCreate(BaseModel):
    type: str
    title: str
    description: str
    song_id: int

class RecommendationOut(BaseModel):
    id: int
    type: str
    title: str
    description: str
    song_id: int
    class Config:
        from_attributes = True
