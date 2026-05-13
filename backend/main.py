import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from database import Base, engine
from routes import router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONT_DIR = os.path.join(os.path.dirname(BASE_DIR), "front")
STATIC_DIR = os.path.join(FRONT_DIR, "static")

app = FastAPI(title="Helpdesk Local", docs_url="/docs", redoc_url=None)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

Base.metadata.create_all(bind=engine)
app.include_router(router)


@app.get("/", response_class=FileResponse)
async def home():
    return FileResponse(os.path.join(FRONT_DIR, "index.html"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
