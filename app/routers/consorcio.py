from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/consorcio",
    tags=["consorcio"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.consorcio.Consorcio)
def create_consorcio(
    consorcio: schemas.consorcio.ConsorcioCreate,
    db: Session = Depends(get_db)
):
    return crud.consorcio.create_consorcio(db, consorcio)

@router.get("/", response_model=List[schemas.consorcio.Consorcio])
def read_consorcios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.consorcio.get_consorcios(db, skip, limit)

@router.get("/{consorcio_id}", response_model=schemas.consorcio.Consorcio)
def read_consorcio(
    consorcio_id: int,
    db: Session = Depends(get_db)
):
    db_cons = crud.consorcio.get_consorcio(db, consorcio_id)
    if not db_cons:
        raise HTTPException(status_code=404, detail="Consórcio não encontrado")
    return db_cons

@router.put("/{consorcio_id}", response_model=schemas.consorcio.Consorcio)
def update_consorcio(
    consorcio_id: int,
    consorcio: schemas.consorcio.ConsorcioUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.consorcio.update_consorcio(db, consorcio_id, consorcio)
    if not updated:
        raise HTTPException(status_code=404, detail="Consórcio não encontrado")
    return updated

@router.delete("/{consorcio_id}", response_model=schemas.consorcio.Consorcio)
def delete_consorcio(
    consorcio_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.consorcio.delete_consorcio(db, consorcio_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Consórcio não encontrado")
    return deleted

@router.get("/search/dia_pg/", response_model=List[schemas.consorcio.Consorcio])
def search_by_dia_pg(
    dia_pg: str = Query(..., description="Dia de pagamento"),
    db: Session = Depends(get_db)
):
    return crud.consorcio.get_consorcios_by_dia_pg(db, dia_pg)

@router.get("/search/proposta/", response_model=List[schemas.consorcio.Consorcio])
def search_by_proposta(
    proposta: str = Query(..., description="Proposta"),
    db: Session = Depends(get_db)
):
    return crud.consorcio.get_consorcios_by_proposta(db, proposta)
