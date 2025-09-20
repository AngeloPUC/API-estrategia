# app/routers/agenda.py
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/agenda",
    tags=["agenda"],
)

@router.post("/", response_model=schemas.agenda.Agenda)
def create_agenda(
    agenda: schemas.agenda.AgendaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.agenda.create_agenda(db, agenda, owner_email=owner_email)

@router.get("/", response_model=List[schemas.agenda.Agenda])
def read_agendas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.agenda.get_agendas(db, owner_email=owner_email, skip=skip, limit=limit)

@router.get("/{agenda_id}", response_model=schemas.agenda.Agenda)
def read_agenda(
    agenda_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    db_row = crud.agenda.get_agenda(db, agenda_id, owner_email=owner_email)
    if not db_row:
        raise HTTPException(status_code=404, detail="Registro da agenda não encontrado")
    return db_row

@router.put("/{agenda_id}", response_model=schemas.agenda.Agenda)
def update_agenda(
    agenda_id: int,
    agenda: schemas.agenda.AgendaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    updated = crud.agenda.update_agenda(db, agenda_id, agenda, owner_email=owner_email)
    if not updated:
        raise HTTPException(status_code=404, detail="Registro da agenda não encontrado")
    return updated

@router.delete("/{agenda_id}", response_model=schemas.agenda.Agenda)
def delete_agenda(
    agenda_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    deleted = crud.agenda.delete_agenda(db, agenda_id, owner_email=owner_email)
    if not deleted:
        raise HTTPException(status_code=404, detail="Registro da agenda não encontrado")
    return deleted

@router.get("/search/data/", response_model=List[schemas.agenda.Agenda])
def search_by_data(
    data: date = Query(..., description="Data (formato YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.agenda.get_agendas_by_date(db, owner_email=owner_email, data=data)
