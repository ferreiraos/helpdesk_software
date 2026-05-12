from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Chamado(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    descricao = Column(String)
    status = Column(String, default="aberto")

    feedbacks = relationship("Feedback", back_populates="chamado")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)  # 1 a 5
    comentario = Column(String)

    chamado_id = Column(Integer, ForeignKey("chamados.id"))

    chamado = relationship("Chamado", back_populates="feedbacks")