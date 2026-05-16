from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import (
    FeedbackCreate,
    FeedbackRead,
    MessageCreate,
    MessageRead,
    StatusUpdate,
    TicketCreate,
    TicketDetail,
    TicketSummary,
)
from backend.services import (
    add_feedback,
    add_message,
    create_ticket,
    get_all_tickets,
    get_ticket,
    update_ticket_status,
)

router = APIRouter(prefix="/api")


@router.get("/chamados", response_model=List[TicketSummary])
def list_tickets(db: Session = Depends(get_db)):
    tickets = get_all_tickets(db)
    return [TicketSummary.from_orm(ticket) for ticket in tickets]


@router.get("/chamados/{ticket_id}", response_model=TicketDetail)
def get_ticket_detail(ticket_id: int, db: Session = Depends(get_db)):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return TicketDetail.from_orm(ticket)


@router.post("/chamados", response_model=TicketSummary, status_code=201)
def create_new_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    created = create_ticket(db, ticket)
    return TicketSummary.from_orm(created)


@router.patch("/chamados/{ticket_id}/status", response_model=TicketDetail)
def change_ticket_status(ticket_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    try:
        updated = update_ticket_status(db, ticket_id, status_update)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return TicketDetail.from_orm(updated)


@router.post("/chamados/{ticket_id}/messages", response_model=MessageRead)
def post_message(ticket_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    try:
        created = add_message(db, ticket_id, message)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return MessageRead.from_orm(created)


@router.post("/chamados/{ticket_id}/feedback", response_model=FeedbackRead)
def post_feedback(ticket_id: int, feedback: FeedbackCreate, db: Session = Depends(get_db)):
    try:
        created = add_feedback(db, ticket_id, feedback)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return FeedbackRead.from_orm(created)
