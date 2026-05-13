from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os

from database import SessionLocal
from models import Chamado, Feedback

router = APIRouter()

# Definir o caminho absoluto para os templates
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(os.path.dirname(base_dir), "front", "templates")
templates = Jinja2Templates(directory=templates_dir)


def get_db():
    return SessionLocal()


@router.get("/")
def home(request: Request):
    db = get_db()
    chamados = db.query(Chamado).all()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "chamados": chamados
    })


@router.post("/chamados")
def criar_chamado(
    titulo: str = Form(...),
    descricao: str = Form(...)
):
    db = get_db()

    chamado = Chamado(
        titulo=titulo,
        descricao=descricao,
        status="aberto"
    )

    db.add(chamado)
    db.commit()

    return RedirectResponse("/", status_code=303)


@router.get("/fechar/{id}")
def fechar_chamado(id: int):
    db = get_db()

    chamado = db.query(Chamado).filter(Chamado.id == id).first()
    chamado.status = "fechado"

    db.commit()

    return RedirectResponse("/", status_code=303)


@router.post("/feedback/{id}")
def adicionar_feedback(
    id: int,
    rating: int = Form(...),
    comentario: str = Form(...)
):
    db = get_db()

    chamado = db.query(Chamado).filter(Chamado.id == id).first()
    if not chamado or chamado.status != "fechado":
        return RedirectResponse("/", status_code=303)  # ou erro

    feedback = Feedback(
        rating=rating,
        comentario=comentario,
        chamado_id=id
    )

    db.add(feedback)
    db.commit()

    return RedirectResponse("/", status_code=303)


@router.get("/feedback/{id}")
def ver_feedback(id: int, request: Request):
    db = get_db()

    chamado = db.query(Chamado).filter(Chamado.id == id).first()
    feedbacks = chamado.feedbacks if chamado else []

    return templates.TemplateResponse("feedback.html", {
        "request": request,
        "chamado": chamado,
        "feedbacks": feedbacks
    })


@router.get("/admin/feedbacks")
def admin_feedbacks(request: Request):
    db = get_db()

    feedbacks = db.query(Feedback).all()
    chamados = {f.chamado_id: f.chamado for f in feedbacks}

    return templates.TemplateResponse("admin_feedbacks.html", {
        "request": request,
        "feedbacks": feedbacks,
        "chamados": chamados
    })