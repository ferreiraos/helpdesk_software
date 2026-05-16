from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from backend.models import Chamado, Feedback, Mensagem, StatusHistory
from backend.schemas import FeedbackCreate, MessageCreate, StatusUpdate, TicketCreate


ALLOWED_STATUSES = {"aberto", "em andamento", "resolvido"}


def _normalize_ticket_timestamps(ticket: Chamado) -> Chamado:
    if ticket.created_at is None:
        ticket.created_at = ticket.updated_at or datetime.utcnow()
    if ticket.updated_at is None:
        ticket.updated_at = ticket.created_at or datetime.utcnow()
    return ticket


def get_all_tickets(db: Session) -> List[Chamado]:
    tickets = db.query(Chamado).order_by(Chamado.updated_at.desc()).all()
    return [_normalize_ticket_timestamps(ticket) for ticket in tickets]


def get_ticket(db: Session, ticket_id: int) -> Optional[Chamado]:
    ticket = db.query(Chamado).filter(Chamado.id == ticket_id).first()
    return _normalize_ticket_timestamps(ticket) if ticket else None


def create_ticket(db: Session, ticket: TicketCreate) -> Chamado:
    chamado = Chamado(
        titulo=ticket.titulo.strip(),
        descricao=ticket.descricao.strip(),
        status="aberto",
    )
    db.add(chamado)
    db.commit()
    db.refresh(chamado)
    return chamado


def update_ticket_status(db: Session, ticket_id: int, status_update: StatusUpdate) -> Chamado:
    chamado = get_ticket(db, ticket_id)
    if not chamado:
        raise ValueError("Chamado não encontrado")

    new_status = status_update.status.strip().lower()
    if new_status not in ALLOWED_STATUSES:
        raise ValueError("Status inválido")

    if chamado.status != new_status:
        history = StatusHistory(
            chamado_id=chamado.id,
            previous_status=chamado.status,
            new_status=new_status,
            note=f"Status alterado de {chamado.status} para {new_status}",
        )
        chamado.status = new_status
        chamado.updated_at = datetime.utcnow()
        db.add(history)
        db.commit()
        db.refresh(chamado)

    return chamado


def add_message(db: Session, ticket_id: int, message: MessageCreate) -> Mensagem:
    chamado = get_ticket(db, ticket_id)
    if not chamado:
        raise ValueError("Chamado não encontrado")

    mensagem = Mensagem(
        chamado_id=chamado.id,
        author=message.author.strip() or "Usuário",
        content=message.content.strip(),
    )
    db.add(mensagem)
    chamado.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(mensagem)
    return mensagem


def add_feedback(db: Session, ticket_id: int, feedback_data: FeedbackCreate) -> Feedback:
    chamado = get_ticket(db, ticket_id)
    if not chamado:
        raise ValueError("Chamado não encontrado")

    if chamado.status != "resolvido":
        raise ValueError("Feedback só pode ser registrado após a resolução do chamado")

    if chamado.feedback:
        raise ValueError("Feedback já registrado para este chamado")

    feedback = Feedback(
        chamado_id=chamado.id,
        rating=feedback_data.rating,
        comentario=feedback_data.comentario.strip() if feedback_data.comentario else None,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback
