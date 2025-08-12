from pydantic import BaseModel
from datetime import date
from typing import Optional

class AcoesBase(BaseModel):
    titulo: str
    base: str
    descricao: Optional[str] = None
    dt_venc: Optional[date] = None
    quem_id: int

class AcoesCreate(AcoesBase):
    pass

class AcoesUpdate(BaseModel):
    titulo: Optional[str] = None
    base: Optional[str] = None
    descricao: Optional[str] = None
    dt_venc: Optional[date] = None
    quem_id: Optional[int] = None

class Acoes(AcoesBase):
    id: int

    class Config:
        orm_mode = True
