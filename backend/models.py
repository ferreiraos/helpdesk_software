from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from database import Base


class Chamado(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    status = Column(String, default="aberto", nullable=False)

    messages = relationship(
        "Message",
        back_populates="chamado",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    feedbacks = relationship(
        "Feedback",
        back_populates="chamado",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    history = relationship(
        "StatusHistory",
        back_populates="chamado",
        cascade="all, delete-orphan",
        lazy="joined",
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)
    author = Column(String, nullable=False, default="Usuário")
    content = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    chamado = relationship("Chamado", back_populates="messages")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comentario = Column(String, nullable=True)

    chamado = relationship("Chamado", back_populates="feedbacks")


class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True, index=True)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)
    status = Column(String, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    chamado = relationship("Chamado", back_populates="history")
