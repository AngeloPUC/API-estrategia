from sqlalchemy import Column, Integer, Text, Date
from app.database import Base

class Tdv(Base):
    __tablename__ = "tdv"

    id = Column(Integer, primary_key=True, index=True)
    proposta = Column(Text, nullable=False)
    n_meses = Column(Text, nullable=False)
    dia_venc = Column(Text, nullable=False)
    pmt_pontos = Column(Text, nullable=False)
    dt_venda = Column(Date, nullable=True)
