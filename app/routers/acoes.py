from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/acoes",
    tags=["acoes"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.acoes.Acoes)
def create_acao(
    acao: schemas.acoes.AcoesCreate,
    db: Session = Depends(get_db)
):
    return crud.acoes.create_acao(db, acao)

@router.get("/", response_model=List[schemas.acoes.Acoes])
def read_acoes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.acoes.get_acoes(db, skip, limit)

@router.get("/{acao_id}", response_model=schemas.acoes.Acoes)
def read_acao(
    acao_id: int,
    db: Session = Depends(get_db)
):
    db_acao = crud.acoes.get_acao(db, acao_id)
    if not db_acao:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return db_acao

@router.put("/{acao_id}", response_model=schemas.acoes.Acoes)
def update_acao(
    acao_id: int,
    acao: schemas.acoes.AcoesUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.acoes.update_acao(db, acao_id, acao)
    if not updated:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return updated

@router.delete("/{acao_id}", response_model=schemas.acoes.Acoes)
def delete_acao(
    acao_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.acoes.delete_acao(db, acao_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return deleted

@router.get("/search/", response_model=List[schemas.acoes.Acoes])
def search_acoes(
    quem_id: int = Query(..., description="ID do responsável"),
    dt_venc: date = Query(..., description="Data de vencimento"),
    db: Session = Depends(get_db)
):
    return crud.acoes.get_acoes_by_quem_id_and_dt_venc(db, quem_id, dt_venc)
