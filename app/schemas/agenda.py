from datetime import date
from typing import Optional
from pydantic import BaseModel, constr


class AgendaBase(BaseModel):
    titulo: constr(strip_whitespace=True, min_length=1)
    data: Optional[date] = None
    hora: Optional[str] = None
    obs: Optional[str] = None


class AgendaCreate(AgendaBase):
    pass


class AgendaUpdate(BaseModel):
    titulo: Optional[constr(strip_whitespace=True, min_length=1)] = None
    data: Optional[date] = None
    hora: Optional[str] = None
    obs: Optional[str] = None


class Agenda(AgendaBase):
    id: int
    dono: Optional[str] = None

    class Config:
        orm_mode = True
