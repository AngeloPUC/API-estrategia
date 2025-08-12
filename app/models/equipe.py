from sqlalchemy import Column, Integer, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Equipe(Base):
    __tablename__ = "equipe"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(Text, nullable=False)
    funcao = Column(Text, nullable=False)
    dt_niver = Column(Date, nullable=True)

    acoes = relationship("Acoes", back_populates="owner")
    feedbacks = relationship("Feedback", back_populates="owner")
