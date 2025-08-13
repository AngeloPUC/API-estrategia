# app/models/acoes.py

from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Acoes(Base):
    __tablename__ = "acoes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(Text, nullable=False)
    base = Column(Text, nullable=False)
    descricao = Column(Text, nullable=True)
    dt_venc = Column(Date, nullable=True)
    quem_id = Column(Integer, ForeignKey("equipe.id"), nullable=False)

    # identifica o usuário dono deste registro
    dono = Column(Text, nullable=False, index=True)

    owner = relationship("Equipe", back_populates="acoes")
