# app/schemas/tarefas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional

class TarefasBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    dt_venc: Optional[date] = None

class TarefasCreate(TarefasBase):
    pass

class TarefasUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    dt_venc: Optional[date] = None

class Tarefas(TarefasBase):
    id: int
    dono: str

    class Config:
        from_attributes = True
