# app/routers/agenda.py
from datetime import date, datetime, time as time_cls
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

def _compose_datetime(data_field, hora_field):
    """
    Recebe data_field (date | str | None) e hora_field (str | None).
    Retorna datetime ou None.
    """
    if not data_field:
        return None
    # data_field pode ser objeto date ou string 'YYYY-MM-DD'
    if isinstance(data_field, str):
        data_str = data_field
    else:
        # date -> ISO date
        data_str = data_field.isoformat()
    if hora_field:
        # hora esperada no formato 'HH:MM'
        try:
            # cria datetime local (assume hora local)
            dt = datetime.fromisoformat(f"{data_str}T{hora_field}")
            return dt
        except Exception:
            # fallback: tentar parse manual
            parts = hora_field.split(':')
            h = int(parts[0]) if parts and parts[0].isdigit() else 0
            m = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
            return datetime.fromisoformat(f"{data_str}T00:00").replace(hour=h, minute=m)
    # sem hora: usar meia-noite do dia
    return datetime.fromisoformat(f"{data_str}T00:00:00")

@router.post("/", response_model=schemas.agenda.Agenda)
def create_agenda(
    agenda: schemas.agenda.AgendaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]

    # preparar payload: converte data+hora para datetime se fornecidos
    payload = agenda.dict(exclude_unset=True)
    # extrair campos possivelmente presentes
    data_field = payload.get("data")
    hora_field = payload.get("hora")
    if data_field is not None:
        try:
            payload["data"] = _compose_datetime(data_field, hora_field)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Formato de data/hora inválido: {e}")

    return crud.agenda.create_agenda(db, schemas.agenda.AgendaCreate(**payload), owner_email=owner_email)

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

    payload = agenda.dict(exclude_unset=True)
    data_field = payload.get("data")
    hora_field = payload.get("hora")
    if data_field is not None:
        try:
            payload["data"] = _compose_datetime(data_field, hora_field)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Formato de data/hora inválido: {e}")

    updated = crud.agenda.update_agenda(db, agenda_id, schemas.agenda.AgendaUpdate(**payload), owner_email=owner_email)
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
