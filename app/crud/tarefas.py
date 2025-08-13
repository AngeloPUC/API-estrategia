# app/crud/tarefas.py

from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.models.tarefas import Tarefas as TarefasModel
from app.schemas.tarefas import TarefasCreate, TarefasUpdate

def get_tarefas(
    db: Session,
    dono: str,
    skip: int = 0,
    limit: int = 100
) -> List[TarefasModel]:
    return (
        db.query(TarefasModel)
          .filter(TarefasModel.dono == dono)
          .offset(skip)
          .limit(limit)
          .all()
    )

def get_tarefa(
    db: Session,
    tarefa_id: int,
    dono: str
) -> TarefasModel | None:
    return (
        db.query(TarefasModel)
          .filter(
              TarefasModel.id == tarefa_id,
              TarefasModel.dono == dono
          )
          .first()
    )

def create_tarefa(
    db: Session,
    tarefa: TarefasCreate,
    dono: str
) -> TarefasModel:
    db_tarefa = TarefasModel(**tarefa.dict(), dono=dono)
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

def update_tarefa(
    db: Session,
    tarefa_id: int,
    tarefa_upd: TarefasUpdate,
    dono: str
) -> TarefasModel | None:
    db_tarefa = get_tarefa(db, tarefa_id, dono)
    if not db_tarefa:
        return None

    for key, value in tarefa_upd.dict(exclude_unset=True).items():
        setattr(db_tarefa, key, value)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

def delete_tarefa(
    db: Session,
    tarefa_id: int,
    dono: str
) -> TarefasModel | None:
    db_tarefa = get_tarefa(db, tarefa_id, dono)
    if not db_tarefa:
        return None

    db.delete(db_tarefa)
    db.commit()
    return db_tarefa

def get_tarefas_by_dt_venc(
    db: Session,
    dono: str,
    dt_venc: date
) -> List[TarefasModel]:
    return (
        db.query(TarefasModel)
          .filter(
              TarefasModel.dono == dono,
              TarefasModel.dt_venc == dt_venc
          )
          .all()
    )
