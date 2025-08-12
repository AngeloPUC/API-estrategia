from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/tdv",
    tags=["tdv"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.tdv.Tdv)
def create_tdv(
    tdv: schemas.tdv.TdvCreate,
    db: Session = Depends(get_db)
):
    return crud.tdv.create_tdv(db, tdv)

@router.get("/", response_model=List[schemas.tdv.Tdv])
def read_tdvs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.tdv.get_tdvs(db, skip, limit)

@router.get("/{tdv_id}", response_model=schemas.tdv.Tdv)
def read_tdv(
    tdv_id: int,
    db: Session = Depends(get_db)
):
    db_tdv = crud.tdv.get_tdv(db, tdv_id)
    if not db_tdv:
        raise HTTPException(status_code=404, detail="TDV não encontrada")
    return db_tdv

@router.put("/{tdv_id}", response_model=schemas.tdv.Tdv)
def update_tdv(
    tdv_id: int,
    tdv: schemas.tdv.TdvUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.tdv.update_tdv(db, tdv_id, tdv)
    if not updated:
        raise HTTPException(status_code=404, detail="TDV não encontrada")
    return updated

@router.delete("/{tdv_id}", response_model=schemas.tdv.Tdv)
def delete_tdv(
    tdv_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.tdv.delete_tdv(db, tdv_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="TDV não encontrada")
    return deleted

@router.get("/search/dia_venc/", response_model=List[schemas.tdv.Tdv])
def search_by_dia_venc(
    dia_venc: str = Query(..., description="Dia de vencimento"),
    db: Session = Depends(get_db)
):
    return crud.tdv.get_tdvs_by_dia_venc(db, dia_venc)

@router.get("/search/proposta/", response_model=List[schemas.tdv.Tdv])
def search_by_proposta(
    proposta: str = Query(..., description="Proposta"),
    db: Session = Depends(get_db)
):
    return crud.tdv.get_tdvs_by_proposta(db, proposta)
