from pydantic import BaseModel

class SongCreate(BaseModel):
    title: str
    artist: str

class SongOut(BaseModel):
    id: int
    title: str
    artist: str
    class Config:
        from_attributes = True
