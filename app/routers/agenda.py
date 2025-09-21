from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/agenda",
    tags=["agenda"],
)


def _validate_date_str(d: str) -> date:
    """
    Valida string 'YYYY-MM-DD' e retorna objeto date.
    Lança ValueError se inválido.
    """
    try:
        return date.fromisoformat(d)
    except Exception as e:
        raise ValueError(f"data inválida: {e}")


def _validate_time_str(t: str) -> str:
    """
    Garante que t é 'HH:MM' e retorna no formato zero-padded.
    Lança ValueError se inválido.
    """
    if t is None or t == "":
        raise ValueError("hora vazia")
    parts = str(t).split(":")
    if len(parts) == 0:
        raise ValueError("formato de hora inválido")
    try:
        h = int(parts[0])
        m = int(parts[1]) if len(parts) > 1 else 0
    except Exception:
        raise ValueError("hora contém partes não numéricas")
    if not (0 <= h <= 23 and 0 <= m <= 59):
        raise ValueError("hora fora do intervalo 00:00-23:59")
    return f"{str(h).zfill(2)}:{str(m).zfill(2)}"


@router.post("/", response_model=schemas.agenda.Agenda)
def create_agenda(
    agenda: schemas.agenda.AgendaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create agenda:
    - Normaliza data para objeto date (se fornecida)
    - Normaliza hora para string 'HH:MM' (se fornecida)
    - Não converte para datetime; mantém tipos compatíveis com schema e modelo
    """
    owner_email = current_user["email"]
    payload = agenda.dict(exclude_unset=True)

    # Normaliza data -> date
    data_field = payload.get("data")
    if data_field is not None and data_field != "":
        if isinstance(data_field, (date, datetime)):
            payload["data"] = data_field if isinstance(data_field, date) else data_field.date()
        else:
            try:
                payload["data"] = _validate_date_str(str(data_field))
            except Exception as e:
                raise HTTPException(status_code=422, detail=f"Formato de data inválido: {e}")

    # Normaliza hora -> 'HH:MM' ou remove
    hora_field = payload.get("hora")
    if hora_field is not None and hora_field != "":
        try:
            payload["hora"] = _validate_time_str(str(hora_field))
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Formato de hora inválido: {e}")
    else:
        payload.pop("hora", None)

    try:
        created = crud.agenda.create_agenda(db, schemas.agenda.AgendaCreate(**payload), owner_email=owner_email)
        return created
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print("ERROR create_agenda:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro interno ao criar agenda")


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
    """
    Atualiza um agendamento. Normalização igual ao create.
    """
    owner_email = current_user["email"]
    payload = agenda.dict(exclude_unset=True)

    # Normaliza data
    data_field = payload.get("data")
    if data_field is not None and data_field != "":
        if isinstance(data_field, (date, datetime)):
            payload["data"] = data_field if isinstance(data_field, date) else data_field.date()
        else:
            try:
                payload["data"] = _validate_date_str(str(data_field))
            except Exception as e:
                raise HTTPException(status_code=422, detail=f"Formato de data inválido: {e}")
    else:
        if "data" in payload and payload["data"] in (None, ""):
            payload.pop("data", None)

    # Normaliza hora
    hora_field = payload.get("hora")
    if hora_field is not None and hora_field != "":
        try:
            payload["hora"] = _validate_time_str(str(hora_field))
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Formato de hora inválido: {e}")
    else:
        if "hora" in payload and payload["hora"] in (None, ""):
            payload.pop("hora", None)

    try:
        updated = crud.agenda.update_agenda(db, agenda_id, schemas.agenda.AgendaUpdate(**payload), owner_email=owner_email)
        if not updated:
            raise HTTPException(status_code=404, detail="Registro da agenda não encontrado")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print("ERROR update_agenda:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar agenda")


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
