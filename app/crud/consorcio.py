from sqlalchemy.orm import Session
from typing import List

from app.models.consorcio import Consorcio as ConsorcioModel
from app.schemas.consorcio import ConsorcioCreate, ConsorcioUpdate

def get_consorcios(db: Session, skip: int = 0, limit: int = 100) -> List[ConsorcioModel]:
    return db.query(ConsorcioModel).offset(skip).limit(limit).all()

def get_consorcio(db: Session, consorcio_id: int) -> ConsorcioModel | None:
    return db.query(ConsorcioModel).filter(ConsorcioModel.id == consorcio_id).first()

def create_consorcio(db: Session, consorcio: ConsorcioCreate) -> ConsorcioModel:
    db_cons = ConsorcioModel(**consorcio.dict())
    db.add(db_cons)
    db.commit()
    db.refresh(db_cons)
    return db_cons

def update_consorcio(db: Session, consorcio_id: int, consorcio: ConsorcioUpdate) -> ConsorcioModel | None:
    db_cons = get_consorcio(db, consorcio_id)
    if not db_cons:
        return None
    update_data = consorcio.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cons, key, value)
    db.commit()
    db.refresh(db_cons)
    return db_cons

def delete_consorcio(db: Session, consorcio_id: int) -> ConsorcioModel | None:
    db_cons = get_consorcio(db, consorcio_id)
    if not db_cons:
        return None
    db.delete(db_cons)
    db.commit()
    return db_cons

def get_consorcios_by_dia_pg(db: Session, dia_pg: str) -> List[ConsorcioModel]:
    return db.query(ConsorcioModel).filter(ConsorcioModel.dia_pg == dia_pg).all()

def get_consorcios_by_proposta(db: Session, proposta: str) -> List[ConsorcioModel]:
    return db.query(ConsorcioModel).filter(ConsorcioModel.proposta == proposta).all()
