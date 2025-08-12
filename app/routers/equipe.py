from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/equipe",
    tags=["equipe"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.equipe.Equipe)
def create_equipe(
    equipe: schemas.equipe.EquipeCreate,
    db: Session = Depends(get_db)
):
    return crud.equipe.create_equipe(db, equipe)

@router.get("/", response_model=List[schemas.equipe.Equipe])
def read_equipes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.equipe.get_equipes(db, skip, limit)

@router.get("/{equipe_id}", response_model=schemas.equipe.Equipe)
def read_equipe(
    equipe_id: int,
    db: Session = Depends(get_db)
):
    db_equipe = crud.equipe.get_equipe(db, equipe_id)
    if not db_equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    return db_equipe

@router.put("/{equipe_id}", response_model=schemas.equipe.Equipe)
def update_equipe(
    equipe_id: int,
    equipe: schemas.equipe.EquipeUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.equipe.update_equipe(db, equipe_id, equipe)
    if not updated:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    return updated

@router.delete("/{equipe_id}", response_model=schemas.equipe.Equipe)
def delete_equipe(
    equipe_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.equipe.delete_equipe(db, equipe_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    return deleted

@router.get("/search/", response_model=List[schemas.equipe.Equipe])
def search_equipes(
    funcao: str = Query(..., description="Função na equipe"),
    dt_niver: date = Query(..., description="Data de aniversário"),
    db: Session = Depends(get_db)
):
    return crud.equipe.get_equipes_by_funcao_and_dt_niver(db, funcao, dt_niver)
