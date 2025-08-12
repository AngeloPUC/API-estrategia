import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carrega .env
load_dotenv()

# Lê a string de conexão
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Defina DATABASE_URL no .env")

# Cria o engine com SSL obrigatório
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},  # Neon exige SSL
    echo=False,
    future=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
