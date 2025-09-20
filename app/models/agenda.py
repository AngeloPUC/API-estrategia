from sqlalchemy import Column, Integer, Text, Date
from app.database import Base

class Agenda(Base):
    __tablename__ = "agenda"  # nome da tabela no Neon

    id = Column(Integer, primary_key=True, index=True)
    # colunas no Neon: Titulo, Data, hora, obs, dono
    titulo = Column('Titulo', Text, nullable=False)
    data = Column('Data', Date, nullable=True)
    hora = Column('hora', Text, nullable=True)
    obs = Column('obs', Text, nullable=True)
    dono = Column('dono', Text, nullable=True, index=True)
