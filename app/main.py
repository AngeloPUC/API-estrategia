from fastapi import FastAPI
from app.routers import acoes, equipe, consorcio, tarefas, tdv, feedback

app = FastAPI(title="API Estratégia", version="1.0")

# Incluindo rotas
app.include_router(acoes.router)
app.include_router(equipe.router)
app.include_router(consorcio.router)
app.include_router(tarefas.router)
app.include_router(tdv.router)
app.include_router(feedback.router)
