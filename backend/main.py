from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from backend.database import Base, ensure_sqlite_column, engine
from backend.routes import router

DEFAULT_TIMESTAMP_TYPE = "DATETIME DEFAULT CURRENT_TIMESTAMP"

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "front" / "templates"
STATIC_DIR = BASE_DIR / "front" / "static"

app = FastAPI(title="Helpdesk Local", debug=True)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "front" / "static")),
    name="static",
)

app.include_router(router)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    ensure_sqlite_column(engine, "chamados", "created_at", DEFAULT_TIMESTAMP_TYPE)
    ensure_sqlite_column(engine, "chamados", "updated_at", DEFAULT_TIMESTAMP_TYPE)
    ensure_sqlite_column(engine, "feedbacks", "comentario", "TEXT")
    ensure_sqlite_column(engine, "feedbacks", "chamado_id", "INTEGER")
    ensure_sqlite_column(engine, "feedbacks", "created_at", DEFAULT_TIMESTAMP_TYPE)
    ensure_sqlite_column(engine, "mensagens", "created_at", DEFAULT_TIMESTAMP_TYPE)
    ensure_sqlite_column(engine, "status_history", "created_at", DEFAULT_TIMESTAMP_TYPE)

    with engine.connect() as connection:
        connection.execute(
            text(
                "UPDATE chamados SET created_at = COALESCE(created_at, updated_at, CURRENT_TIMESTAMP) "
                "WHERE created_at IS NULL"
            )
        )
        connection.execute(
            text(
                "UPDATE chamados SET updated_at = COALESCE(updated_at, created_at, CURRENT_TIMESTAMP) "
                "WHERE updated_at IS NULL"
            )
        )
        connection.execute(text("UPDATE feedbacks SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"))
        connection.execute(text("UPDATE mensagens SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"))
        connection.execute(text("UPDATE status_history SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"))
        connection.commit()


@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(str(TEMPLATE_DIR / "index.html"))