from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(Text, nullable=False)
    base = Column(Text, nullable=False)
    descricao = Column(Text, nullable=True)
    resultado = Column(Integer, nullable=False)
    quem_id = Column(Integer, ForeignKey("equipe.id"), nullable=False)
    feedback = Column(Text, nullable=True)

    owner = relationship("Equipe", back_populates="feedbacks")
