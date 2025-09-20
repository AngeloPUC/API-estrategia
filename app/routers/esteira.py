# app/routers/esteira.py
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/esteira",
    tags=["esteira"],
)

@router.post("/", response_model=schemas.esteira.Esteira)
def create_esteira(
    esteira: schemas.esteira.EsteiraCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.esteira.create_esteira(
        db,
        esteira,
        owner_email=owner_email,
    )

@router.get("/", response_model=List[schemas.esteira.Esteira])
def read_esteiras(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.esteira.get_esteiras(
        db,
        owner_email=owner_email,
        skip=skip,
        limit=limit,
    )

@router.get("/{esteira_id}", response_model=schemas.esteira.Esteira)
def read_esteira(
    esteira_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    db_row = crud.esteira.get_esteira(
        db,
        esteira_id,
        owner_email=owner_email,
    )
    if not db_row:
        raise HTTPException(status_code=404, detail="Registro de esteira não encontrado")
    return db_row

@router.put("/{esteira_id}", response_model=schemas.esteira.Esteira)
def update_esteira(
    esteira_id: int,
    esteira: schemas.esteira.EsteiraUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    updated = crud.esteira.update_esteira(
        db,
        esteira_id,
        esteira,
        owner_email=owner_email,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Registro de esteira não encontrado")
    return updated

@router.delete("/{esteira_id}", response_model=schemas.esteira.Esteira)
def delete_esteira(
    esteira_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    deleted = crud.esteira.delete_esteira(
        db,
        esteira_id,
        owner_email=owner_email,
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Registro de esteira não encontrado")
    return deleted

@router.get("/search/cnpjcpf/", response_model=List[schemas.esteira.Esteira])
def search_by_cnpjcpf(
    cnpjcpf: str = Query(..., description="CNPJ ou CPF"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.esteira.get_esteiras_by_cnpjcpf(
        db,
        owner_email=owner_email,
        cnpjcpf=cnpjcpf,
    )

@router.get("/search/data/", response_model=List[schemas.esteira.Esteira])
def search_by_data(
    data: date = Query(..., description="Data (formato YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.esteira.get_esteiras_by_data(
        db,
        owner_email=owner_email,
        data=data,
    )
