from pydantic import BaseModel
from datetime import date
from typing import Optional

class ConsorcioBase(BaseModel):
    proposta: str
    dt_venda: Optional[date] = None
    tipo: str
    valor: str
    dia_pg: str

class ConsorcioCreate(ConsorcioBase):
    pass

class ConsorcioUpdate(BaseModel):
    proposta: Optional[str] = None
    dt_venda: Optional[date] = None
    tipo: Optional[str] = None
    valor: Optional[str] = None
    dia_pg: Optional[str] = None

class Consorcio(ConsorcioBase):
    id: int

    class Config:
        from_attributes = True
