# app/schemas/esteira.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, condecimal, constr

class EsteiraBase(BaseModel):
    nome: constr(strip_whitespace=True, min_length=1)
    cnpjcpf: Optional[str] = None
    operacao: Optional[str] = None
    valor: Optional[condecimal(max_digits=14, decimal_places=2)] = None
    data: Optional[datetime] = None
    obs: Optional[str] = None

class EsteiraCreate(EsteiraBase):
    # owner_email é atribuído no backend a partir do token, não enviado pelo cliente
    pass

class EsteiraUpdate(BaseModel):
    nome: Optional[constr(strip_whitespace=True, min_length=1)] = None
    cnpjcpf: Optional[str] = None
    operacao: Optional[str] = None
    valor: Optional[condecimal(max_digits=14, decimal_places=2)] = None
    data: Optional[datetime] = None
    obs: Optional[str] = None

class Esteira(EsteiraBase):
    id: int
    owner_email: str

    class Config:
        orm_mode = True
