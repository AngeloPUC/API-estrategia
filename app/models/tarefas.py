from sqlalchemy import Column, Integer, Text, Date
from app.database import Base

class Tarefas(Base):
    __tablename__ = "tarefas"

    id          = Column(Integer, primary_key=True, index=True)
    titulo      = Column(Text,    nullable=False)
    descricao   = Column(Text,    nullable=True)
    dt_venc     = Column(Date,    nullable=True)

    owner_email = Column(
        "dono",
        Text,
        nullable=False,
        index=True,
    )
