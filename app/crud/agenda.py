from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date

from app.models.agenda import Agenda as AgendaModel
from app.schemas.agenda import AgendaCreate, AgendaUpdate


def get_agendas(
    db: Session,
    owner_email: str,
    skip: int = 0,
    limit: int = 100,
) -> List[AgendaModel]:
    return (
        db.query(AgendaModel)
          .filter(AgendaModel.dono == owner_email)
          .offset(skip)
          .limit(limit)
          .all()
    )


def get_agenda(
    db: Session,
    agenda_id: int,
    owner_email: str,
) -> Optional[AgendaModel]:
    return (
        db.query(AgendaModel)
          .filter(AgendaModel.id == agenda_id, AgendaModel.dono == owner_email)
          .first()
    )


def create_agenda(
    db: Session,
    agenda: AgendaCreate,
    owner_email: str,
) -> AgendaModel:
    # agenda é um pydantic model; já normalizamos types no router
    payload = agenda.dict(exclude_unset=True)
    db_row = AgendaModel(**payload, dono=owner_email)
    db.add(db_row)
    db.commit()
    db.refresh(db_row)
    return db_row


def update_agenda(
    db: Session,
    agenda_id: int,
    agenda_upd: AgendaUpdate,
    owner_email: str,
) -> Optional[AgendaModel]:
    db_row = get_agenda(db, agenda_id, owner_email)
    if not db_row:
        return None
    for key, value in agenda_upd.dict(exclude_unset=True).items():
        setattr(db_row, key, value)
    db.commit()
    db.refresh(db_row)
    return db_row


def delete_agenda(
    db: Session,
    agenda_id: int,
    owner_email: str,
) -> Optional[AgendaModel]:
    db_row = get_agenda(db, agenda_id, owner_email)
    if not db_row:
        return None
    db.delete(db_row)
    db.commit()
    return db_row


def get_agendas_by_date(
    db: Session,
    owner_email: str,
    data: date,
) -> List[AgendaModel]:
    return (
        db.query(AgendaModel)
          .filter(AgendaModel.dono == owner_email, AgendaModel.data == data)
          .all()
    )
