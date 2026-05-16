from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.database import Base


class Chamado(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="aberto")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Mensagem", back_populates="chamado", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="chamado", uselist=False, cascade="all, delete-orphan")
    history = relationship("StatusHistory", back_populates="chamado", order_by="StatusHistory.created_at", cascade="all, delete-orphan")

    @property
    def has_feedback(self) -> bool:
        return self.feedback is not None


class Mensagem(Base):
    __tablename__ = "mensagens"

    id = Column(Integer, primary_key=True, index=True)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    chamado = relationship("Chamado", back_populates="messages")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    comentario = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)

    chamado = relationship("Chamado", back_populates="feedback")


class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True, index=True)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)
    previous_status = Column(String(50), nullable=False)
    new_status = Column(String(50), nullable=False)
    note = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    chamado = relationship("Chamado", back_populates="history")