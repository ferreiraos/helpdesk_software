from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    author: str = Field(default="Usuário")
    content: str = Field(..., min_length=1)


class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comentario: Optional[str] = None


class StatusUpdate(BaseModel):
    status: str = Field(..., min_length=1)
    note: Optional[str] = None


class ChamadoCreate(BaseModel):
    titulo: str = Field(..., min_length=3)
    descricao: str = Field(..., min_length=5)


class MessageRead(BaseModel):
    id: int
    author: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class FeedbackRead(BaseModel):
    id: int
    rating: int
    comentario: Optional[str]

    model_config = {"from_attributes": True}


class StatusHistoryRead(BaseModel):
    id: int
    status: str
    note: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class ChamadoRead(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: str
    messages: List[MessageRead] = []
    feedbacks: List[FeedbackRead] = []
    history: List[StatusHistoryRead] = []

    model_config = {"from_attributes": True}
