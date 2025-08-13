from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app import crud, schemas
from app.database import get_db
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/acoes",
    tags=["Ações"],
)

@router.post("/", response_model=schemas.acoes.Acoes)
def create_acao(
    acao: schemas.acoes.AcoesCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.acoes.create_acao(
        db,
        acao,
        owner_email=owner_email
    )

@router.get("/", response_model=List[schemas.acoes.Acoes])
def read_acoes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.acoes.get_acoes(
        db,
        owner_email=owner_email,
        skip=skip,
        limit=limit
    )

@router.get("/{acao_id}", response_model=schemas.acoes.Acoes)
def read_acao(
    acao_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    db_acao = crud.acoes.get_acao(
        db,
        acao_id,
        owner_email=owner_email
    )
    if not db_acao:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return db_acao

@router.put("/{acao_id}", response_model=schemas.acoes.Acoes)
def update_acao(
    acao_id: int,
    acao: schemas.acoes.AcoesUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    updated = crud.acoes.update_acao(
        db,
        acao_id,
        acao,
        owner_email=owner_email
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return updated

@router.delete("/{acao_id}", response_model=schemas.acoes.Acoes)
def delete_acao(
    acao_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    deleted = crud.acoes.delete_acao(
        db,
        acao_id,
        owner_email=owner_email
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return deleted

@router.get("/search/", response_model=List[schemas.acoes.Acoes])
def search_acoes(
    quem_id: int = Query(..., description="ID do responsável"),
    dt_venc: date = Query(..., description="Data de vencimento"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.acoes.get_acoes_by_quem_id_and_dt_venc(
        db,
        owner_email=owner_email,
        quem_id=quem_id,
        dt_venc=dt_venc
    )
