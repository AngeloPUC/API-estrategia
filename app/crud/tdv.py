from sqlalchemy.orm import Session
from typing import List

from app.models.tdv import Tdv as TdvModel
from app.schemas.tdv import TdvCreate, TdvUpdate

def get_tdvs(
    db: Session,
    owner_email: str,
    skip: int = 0,
    limit: int = 100
) -> List[TdvModel]:
    return (
        db.query(TdvModel)
          .filter(TdvModel.owner_email == owner_email)
          .offset(skip)
          .limit(limit)
          .all()
    )

def get_tdv(
    db: Session,
    tdv_id: int,
    owner_email: str
) -> TdvModel | None:
    return (
        db.query(TdvModel)
          .filter(
              TdvModel.id == tdv_id,
              TdvModel.owner_email == owner_email
          )
          .first()
    )

def create_tdv(
    db: Session,
    tdv: TdvCreate,
    owner_email: str
) -> TdvModel:
    db_tdv = TdvModel(**tdv.dict(), owner_email=owner_email)
    db.add(db_tdv)
    db.commit()
    db.refresh(db_tdv)
    return db_tdv

def update_tdv(
    db: Session,
    tdv_id: int,
    tdv_upd: TdvUpdate,
    owner_email: str
) -> TdvModel | None:
    db_tdv = get_tdv(db, tdv_id, owner_email)
    if not db_tdv:
        return None

    for key, value in tdv_upd.dict(exclude_unset=True).items():
        setattr(db_tdv, key, value)
    db.commit()
    db.refresh(db_tdv)
    return db_tdv

def delete_tdv(
    db: Session,
    tdv_id: int,
    owner_email: str
) -> TdvModel | None:
    db_tdv = get_tdv(db, tdv_id, owner_email)
    if not db_tdv:
        return None

    db.delete(db_tdv)
    db.commit()
    return db_tdv

def get_tdvs_by_dia_venc(
    db: Session,
    owner_email: str,
    dia_venc: str
) -> List[TdvModel]:
    return (
        db.query(TdvModel)
          .filter(
              TdvModel.owner_email == owner_email,
              TdvModel.dia_venc == dia_venc
          )
          .all()
    )

def get_tdvs_by_proposta(
    db: Session,
    owner_email: str,
    proposta: str
) -> List[TdvModel]:
    return (
        db.query(TdvModel)
          .filter(
              TdvModel.owner_email == owner_email,
              TdvModel.proposta == proposta
          )
          .all()
    )
