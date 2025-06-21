from fastapi import FastAPI
from models import song, recommendation
from database import engine, Base
from routers.song import router as song_router
from routers.recommendation import router as recommendation_router

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(song_router)
app.include_router(recommendation_router)
