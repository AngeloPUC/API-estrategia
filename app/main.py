# app/main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.database import engine, Base
from app.config import settings
from app.auth.security import get_current_user
from app.routers import acoes, consorcio, equipe, tarefas, tdv, feedback

# cria tabelas em dev
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Estratégia",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# todas as rotas protegidas
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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # 1) define o Bearer JWT nos components
    schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # 2) aplica globalmente
    schema["security"] = [{"bearerAuth": []}]

    # 3) garante que cada operação em cada caminho tenha o security também
    for path_item in schema.get("paths", {}).values():
        for operation in path_item.values():
            operation["security"] = [{"bearerAuth": []}]

    app.openapi_schema = schema
    return app.openapi_schema

# sobrescreve o gerador padrão
app.openapi = custom_openapi
