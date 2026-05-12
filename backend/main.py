from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routes import router

app = FastAPI()

app.mount("/static", StaticFiles(directory="../front/templates"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(router)