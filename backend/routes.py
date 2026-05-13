from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    ChamadoCreate,
    ChamadoRead,
    FeedbackCreate,
    MessageCreate,
    MessageRead,
    StatusUpdate,
    FeedbackRead,
)
from services.chamado_service import (
    add_feedback,
    add_message,
    create_chamado,
    get_all_chamados,
    get_chamado,
    update_chamado_status,
)

router = APIRouter(prefix="/api", tags=["helpdesk"])


@router.get("/chamados", response_model=List[ChamadoRead])
def list_chamados(db: Session = Depends(get_db)):
    return get_all_chamados(db)


@router.post("/chamados", response_model=ChamadoRead, status_code=201)
def create_new_chamado(payload: ChamadoCreate, db: Session = Depends(get_db)):
    return create_chamado(db, payload.titulo, payload.descricao)


@router.get("/chamados/{chamado_id}", response_model=ChamadoRead)
def get_chamado_detail(chamado_id: int, db: Session = Depends(get_db)):
    chamado = get_chamado(db, chamado_id)
    if chamado is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return chamado


@router.put("/chamados/{chamado_id}/status", response_model=ChamadoRead)
def change_chamado_status(
    chamado_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
):
    try:
        chamado = update_chamado_status(db, chamado_id, payload.status, payload.note)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if chamado is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")

    return chamado


@router.post("/chamados/{chamado_id}/messages", response_model=MessageRead)
def post_message(
    chamado_id: int,
    payload: MessageCreate,
    db: Session = Depends(get_db),
):
    message = add_message(db, chamado_id, payload.content, payload.author)
    if message is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return message


@router.post("/chamados/{chamado_id}/feedback", response_model=FeedbackRead)
def post_feedback(
    chamado_id: int,
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
):
    try:
        feedback = add_feedback(db, chamado_id, payload.rating, payload.comentario)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if feedback is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return feedback
