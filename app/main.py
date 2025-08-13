# app/main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.config import settings
from app.auth.security import get_current_user
from app.routers import acoes, consorcio, equipe, tarefas, tdv, feedback

# Cria todas as tabelas (apenas em dev/protótipo)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Estratégia",
    version="1.0"
)

# CORS aberto — ajuste allow_origins para o seu front-end em produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Todas as rotas abaixo dependem do usuário autenticado
common_deps = [Depends(get_current_user)]

app.include_router(acoes.router, dependencies=common_deps)
app.include_router(consorcio.router, dependencies=common_deps)
app.include_router(equipe.router, dependencies=common_deps)
app.include_router(tarefas.router, dependencies=common_deps)
app.include_router(tdv.router, dependencies=common_deps)
app.include_router(feedback.router, dependencies=common_deps)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "API Estratégia rodando e todas as rotas protegidas!"}
