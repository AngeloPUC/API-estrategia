from pydantic import BaseModel
from datetime import date
from typing import Optional

class TdvBase(BaseModel):
    proposta: str
    n_meses: str
    dia_venc: str
    pmt_pontos: str
    dt_venda: Optional[date] = None

class TdvCreate(TdvBase):
    pass

class TdvUpdate(BaseModel):
    proposta: Optional[str] = None
    n_meses: Optional[str] = None
    dia_venc: Optional[str] = None
    pmt_pontos: Optional[str] = None
    dt_venda: Optional[date] = None

class Tdv(TdvBase):
    id: int

    class Config:
        from_attributes = True
