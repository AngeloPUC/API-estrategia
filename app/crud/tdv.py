from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.models.tdv import Tdv as TdvModel
from app.schemas.tdv import TdvCreate, TdvUpdate

def get_tdvs(db: Session, skip: int = 0, limit: int = 100) -> List[TdvModel]:
    return db.query(TdvModel).offset(skip).limit(limit).all()

def get_tdv(db: Session, tdv_id: int) -> TdvModel | None:
    return db.query(TdvModel).filter(TdvModel.id == tdv_id).first()

def create_tdv(db: Session, tdv: TdvCreate) -> TdvModel:
    db_tdv = TdvModel(**tdv.dict())
    db.add(db_tdv)
    db.commit()
    db.refresh(db_tdv)
    return db_tdv

def update_tdv(db: Session, tdv_id: int, tdv: TdvUpdate) -> TdvModel | None:
    db_tdv = get_tdv(db, tdv_id)
    if not db_tdv:
        return None
    update_data = tdv.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tdv, key, value)
    db.commit()
    db.refresh(db_tdv)
    return db_tdv

def delete_tdv(db: Session, tdv_id: int) -> TdvModel | None:
    db_tdv = get_tdv(db, tdv_id)
    if not db_tdv:
        return None
    db.delete(db_tdv)
    db.commit()
    return db_tdv

def get_tdvs_by_dia_venc(db: Session, dia_venc: str) -> List[TdvModel]:
    return db.query(TdvModel).filter(TdvModel.dia_venc == dia_venc).all()

def get_tdvs_by_proposta(db: Session, proposta: str) -> List[TdvModel]:
    return db.query(TdvModel).filter(TdvModel.proposta == proposta).all()
