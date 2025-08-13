# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import settings

# Cria o engine do SQLAlchemy apontando para o seu DATABASE_URL
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"sslmode": "require"},
    echo=False,
    future=True
)

# Configura a Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

# Classe base para os modelos ORM
Base = declarative_base()

# Dependência do FastAPI para injetar a sessão no endpoint
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
