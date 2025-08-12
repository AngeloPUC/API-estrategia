from pydantic import BaseModel
from datetime import date
from typing import Optional

class EquipeBase(BaseModel):
    nome: str
    funcao: str
    dt_niver: Optional[date] = None

class EquipeCreate(EquipeBase):
    pass

class EquipeUpdate(BaseModel):
    nome: Optional[str] = None
    funcao: Optional[str] = None
    dt_niver: Optional[date] = None

class Equipe(EquipeBase):
    id: int

    class Config:
        from_attributes = True
