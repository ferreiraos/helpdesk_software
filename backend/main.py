from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routes import router
import os

app = FastAPI()

# Definir o caminho absoluto para os templates
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(os.path.dirname(base_dir), "front", "templates")

app.mount("/static", StaticFiles(directory=templates_dir), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(router)