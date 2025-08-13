# app/models/consorcio.py

from sqlalchemy import Column, Integer, Text, Date
from app.database import Base

class Consorcio(Base):
    __tablename__ = "consorcio"

    id = Column(Integer, primary_key=True, index=True)
    proposta = Column(Text, nullable=False)
    dt_venda = Column(Date, nullable=True)
    tipo = Column(Text, nullable=False)
    valor = Column(Text, nullable=False)
    dia_pg = Column(Text, nullable=False)

    # identifica o usuário dono deste registro
    dono = Column(Text, nullable=False, index=True)
