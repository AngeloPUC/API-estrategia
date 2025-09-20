# app/models/esteira.py
from sqlalchemy import Column, Integer, Text, Date
from app.database import Base

class Esteira(Base):
    __tablename__ = "Esteira"   # nome exato no Neon

    id = Column(Integer, primary_key=True, index=True)
    nome = Column('nome', Text, nullable=False)
    # coluna do banco chama-se literalmente "CNPJ/CPF"
    cnpjcpf = Column('CNPJ/CPF', Text, nullable=True)
    operacao = Column('operacao', Text, nullable=True)
    # no seu Neon 'valor' é text, manter Text; altere para Numeric se for numeric
    valor = Column('valor', Text, nullable=True)
    data = Column('data', Date, nullable=True)
    obs = Column('obs', Text, nullable=True)
    # mapear a coluna 'dono' para o atributo owner_email usado nos schemas/routers
    owner_email = Column('dono', Text, nullable=True, index=True)
