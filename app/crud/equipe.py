from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.models.equipe import Equipe as EquipeModel
from app.schemas.equipe import EquipeCreate, EquipeUpdate

def get_equipes(db: Session, skip: int = 0, limit: int = 100) -> List[EquipeModel]:
    return db.query(EquipeModel).offset(skip).limit(limit).all()

def get_equipe(db: Session, equipe_id: int) -> EquipeModel | None:
    return db.query(EquipeModel).filter(EquipeModel.id == equipe_id).first()

def create_equipe(db: Session, equipe: EquipeCreate) -> EquipeModel:
    db_equipe = EquipeModel(**equipe.dict())
    db.add(db_equipe)
    db.commit()
    db.refresh(db_equipe)
    return db_equipe

def update_equipe(db: Session, equipe_id: int, equipe: EquipeUpdate) -> EquipeModel | None:
    db_equipe = get_equipe(db, equipe_id)
    if not db_equipe:
        return None
    update_data = equipe.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_equipe, key, value)
    db.commit()
    db.refresh(db_equipe)
    return db_equipe

def delete_equipe(db: Session, equipe_id: int) -> EquipeModel | None:
    db_equipe = get_equipe(db, equipe_id)
    if not db_equipe:
        return None
    db.delete(db_equipe)
    db.commit()
    return db_equipe

def get_equipes_by_funcao_and_dt_niver(
    db: Session, funcao: str, dt_niver: date
) -> List[EquipeModel]:
    return (
        db.query(EquipeModel)
        .filter(EquipeModel.funcao == funcao, EquipeModel.dt_niver == dt_niver)
        .all()
    )
