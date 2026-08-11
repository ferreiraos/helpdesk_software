from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, conint


class MessageCreate(BaseModel):
    author: str = Field(default="Usuário", max_length=100)
    content: str = Field(min_length=1, max_length=1000)


class StatusUpdate(BaseModel):
    status: str


class FeedbackCreate(BaseModel):
    rating: conint(ge=1, le=5)
    comentario: Optional[str] = None


class TicketCreate(BaseModel):
    titulo: str = Field(min_length=3, max_length=200)
    descricao: str = Field(min_length=5, max_length=2000)


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=6)
    full_name: str = Field(min_length=3, max_length=200)
    birth_date: date
    department: Optional[str] = Field(default=None, max_length=100)


class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=6)


class UserRead(BaseModel):
    id: int
    username: str
    full_name: str
    birth_date: date
    department: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageRead(BaseModel):
    id: int
    author: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StatusHistoryRead(BaseModel):
    id: int
    previous_status: str
    new_status: str
    note: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FeedbackRead(BaseModel):
    id: int
    rating: int
    comentario: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketSummary(BaseModel):
    id: int
    titulo: str
    status: str
    created_at: datetime
    updated_at: datetime
    has_feedback: bool = False

    model_config = ConfigDict(from_attributes=True)


class TicketDetail(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageRead] = Field(default_factory=list)
    feedback: Optional[FeedbackRead] = None
    history: List[StatusHistoryRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
