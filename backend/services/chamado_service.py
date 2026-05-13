from sqlalchemy.orm import Session

from models import Chamado, Message, Feedback, StatusHistory

VALID_STATUSES = ["aberto", "em andamento", "resolvido"]


def get_all_chamados(db: Session):
    return db.query(Chamado).order_by(Chamado.id.desc()).all()


def get_chamado(db: Session, chamado_id: int):
    return db.query(Chamado).filter(Chamado.id == chamado_id).first()


def create_chamado(db: Session, titulo: str, descricao: str):
    chamado = Chamado(titulo=titulo, descricao=descricao, status="aberto")
    db.add(chamado)
    db.flush()

    history = StatusHistory(chamado_id=chamado.id, status="aberto", note="Chamado criado")
    db.add(history)
    db.commit()
    db.refresh(chamado)
    return chamado


def update_chamado_status(db: Session, chamado_id: int, status: str, note: str | None = None):
    if status not in VALID_STATUSES:
        raise ValueError("Status inválido")

    chamado = get_chamado(db, chamado_id)
    if chamado is None:
        return None

    chamado.status = status
    history = StatusHistory(chamado_id=chamado.id, status=status, note=note)
    db.add(history)
    db.commit()
    db.refresh(chamado)
    return chamado


def add_message(db: Session, chamado_id: int, content: str, author: str = "Usuário"):
    chamado = get_chamado(db, chamado_id)
    if chamado is None:
        return None

    message = Message(chamado_id=chamado.id, author=author, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def add_feedback(db: Session, chamado_id: int, rating: int, comentario: str | None = None):
    chamado = get_chamado(db, chamado_id)
    if chamado is None:
        return None

    if chamado.status != "resolvido":
        raise ValueError("Feedback só pode ser enviado após resolução")

    feedback = Feedback(chamado_id=chamado.id, rating=rating, comentario=comentario)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback
