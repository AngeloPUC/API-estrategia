# app/routers/consorcio.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/consorcio",
    tags=["Consórcio"],
)

@router.post("/", response_model=schemas.consorcio.Consorcio)
def create_consorcio(
    consorcio: schemas.consorcio.ConsorcioCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.consorcio.create_consorcio(
        db,
        consorcio,
        owner_email=owner_email
    )

@router.get("/", response_model=List[schemas.consorcio.Consorcio])
def read_consorcios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.consorcio.get_consorcios(
        db,
        owner_email=owner_email,
        skip=skip,
        limit=limit
    )

@router.get("/{consorcio_id}", response_model=schemas.consorcio.Consorcio)
def read_consorcio(
    consorcio_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    db_cons = crud.consorcio.get_consorcio(
        db,
        consorcio_id,
        owner_email=owner_email
    )
    if not db_cons:
        raise HTTPException(status_code=404, detail="Consórcio não encontrado")
    return db_cons

@router.put("/{consorcio_id}", response_model=schemas.consorcio.Consorcio)
def update_consorcio(
    consorcio_id: int,
    consorcio: schemas.consorcio.ConsorcioUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    updated = crud.consorcio.update_consorcio(
        db,
        consorcio_id,
        consorcio,
        owner_email=owner_email
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Consórcio não encontrado")
    return updated

@router.delete("/{consorcio_id}", response_model=schemas.consorcio.Consorcio)
def delete_consorcio(
    consorcio_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    deleted = crud.consorcio.delete_consorcio(
        db,
        consorcio_id,
        owner_email=owner_email
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Consórcio não encontrado")
    return deleted

@router.get("/search/dia_pg/", response_model=List[schemas.consorcio.Consorcio])
def search_by_dia_pg(
    dia_pg: str = Query(..., description="Dia de pagamento"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.consorcio.get_consorcios_by_dia_pg(
        db,
        owner_email=owner_email,
        dia_pg=dia_pg
    )

@router.get("/search/proposta/", response_model=List[schemas.consorcio.Consorcio])
def search_by_proposta(
    proposta: str = Query(..., description="Proposta"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.consorcio.get_consorcios_by_proposta(
        db,
        owner_email=owner_email,
        proposta=proposta
    )
