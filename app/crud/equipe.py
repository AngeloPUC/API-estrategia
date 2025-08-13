# app/crud/equipe.py

from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.models.equipe import Equipe as EquipeModel
from app.schemas.equipe import EquipeCreate, EquipeUpdate

def get_equipes(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[EquipeModel]:
    return (
        db.query(EquipeModel)
          .filter(EquipeModel.owner_id == owner_id)
          .offset(skip)
          .limit(limit)
          .all()
    )

def get_equipe(
    db: Session,
    equipe_id: int,
    owner_id: int
) -> EquipeModel | None:
    return (
        db.query(EquipeModel)
          .filter(
              EquipeModel.id == equipe_id,
              EquipeModel.owner_id == owner_id
          )
          .first()
    )

def create_equipe(
    db: Session,
    equipe: EquipeCreate,
    owner_id: int
) -> EquipeModel:
    db_equipe = EquipeModel(**equipe.dict(), owner_id=owner_id)
    db.add(db_equipe)
    db.commit()
    db.refresh(db_equipe)
    return db_equipe

def update_equipe(
    db: Session,
    equipe_id: int,
    equipe_upd: EquipeUpdate,
    owner_id: int
) -> EquipeModel | None:
    db_equipe = get_equipe(db, equipe_id, owner_id)
    if not db_equipe:
        return None

    for key, value in equipe_upd.dict(exclude_unset=True).items():
        setattr(db_equipe, key, value)
    db.commit()
    db.refresh(db_equipe)
    return db_equipe

def delete_equipe(
    db: Session,
    equipe_id: int,
    owner_id: int
) -> EquipeModel | None:
    db_equipe = get_equipe(db, equipe_id, owner_id)
    if not db_equipe:
        return None

    db.delete(db_equipe)
    db.commit()
    return db_equipe

def get_equipes_by_funcao_and_dt_niver(
    db: Session,
    owner_id: int,
    funcao: str,
    dt_niver: date
) -> List[EquipeModel]:
    return (
        db.query(EquipeModel)
          .filter(
              EquipeModel.owner_id == owner_id,
              EquipeModel.funcao == funcao,
              EquipeModel.dt_niver == dt_niver
          )
          .all()
    )
