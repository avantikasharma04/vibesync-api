from fastapi import FastAPI
from app.models import song, recommendation
from app.database import engine, Base
from app.routers.song import router as song_router
from app.routers.recommendation import router as recommendation_router

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(song_router)
app.include_router(recommendation_router)
