# app/crud/consorcio.py

from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.models.consorcio import Consorcio as ConsorcioModel
from app.schemas.consorcio import ConsorcioCreate, ConsorcioUpdate

def get_consorcios(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[ConsorcioModel]:
    return (
        db.query(ConsorcioModel)
          .filter(ConsorcioModel.owner_id == owner_id)
          .offset(skip)
          .limit(limit)
          .all()
    )

def get_consorcio(
    db: Session,
    consorcio_id: int,
    owner_id: int
) -> ConsorcioModel | None:
    return (
        db.query(ConsorcioModel)
          .filter(
              ConsorcioModel.id == consorcio_id,
              ConsorcioModel.owner_id == owner_id
          )
          .first()
    )

def create_consorcio(
    db: Session,
    consorcio: ConsorcioCreate,
    owner_id: int
) -> ConsorcioModel:
    db_cons = ConsorcioModel(**consorcio.dict(), owner_id=owner_id)
    db.add(db_cons)
    db.commit()
    db.refresh(db_cons)
    return db_cons

def update_consorcio(
    db: Session,
    consorcio_id: int,
    consorcio_upd: ConsorcioUpdate,
    owner_id: int
) -> ConsorcioModel | None:
    db_cons = get_consorcio(db, consorcio_id, owner_id)
    if not db_cons:
        return None

    for key, value in consorcio_upd.dict(exclude_unset=True).items():
        setattr(db_cons, key, value)
    db.commit()
    db.refresh(db_cons)
    return db_cons

def delete_consorcio(
    db: Session,
    consorcio_id: int,
    owner_id: int
) -> ConsorcioModel | None:
    db_cons = get_consorcio(db, consorcio_id, owner_id)
    if not db_cons:
        return None

    db.delete(db_cons)
    db.commit()
    return db_cons

def get_consorcios_by_dia_pg(
    db: Session,
    owner_id: int,
    dia_pg: str
) -> List[ConsorcioModel]:
    return (
        db.query(ConsorcioModel)
          .filter(
              ConsorcioModel.owner_id == owner_id,
              ConsorcioModel.dia_pg == dia_pg
          )
          .all()
    )

def get_consorcios_by_proposta(
    db: Session,
    owner_id: int,
    proposta: str
) -> List[ConsorcioModel]:
    return (
        db.query(ConsorcioModel)
          .filter(
              ConsorcioModel.owner_id == owner_id,
              ConsorcioModel.proposta == proposta
          )
          .all()
    )
