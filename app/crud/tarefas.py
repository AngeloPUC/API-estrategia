from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.models.tarefas import Tarefas as TarefasModel
from app.schemas.tarefas import TarefasCreate, TarefasUpdate

def get_tarefas(
    db: Session,
    owner_email: str,
    skip: int = 0,
    limit: int = 100
) -> List[TarefasModel]:
    return (
        db.query(TarefasModel)
          .filter(TarefasModel.owner_email == owner_email)
          .offset(skip)
          .limit(limit)
          .all()
    )

def get_tarefa(
    db: Session,
    tarefa_id: int,
    owner_email: str
) -> TarefasModel | None:
    return (
        db.query(TarefasModel)
          .filter(
              TarefasModel.id == tarefa_id,
              TarefasModel.owner_email == owner_email
          )
          .first()
    )

def create_tarefa(
    db: Session,
    tarefa: TarefasCreate,
    owner_email: str
) -> TarefasModel:
    db_tarefa = TarefasModel(**tarefa.dict(), owner_email=owner_email)
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

def update_tarefa(
    db: Session,
    tarefa_id: int,
    tarefa_upd: TarefasUpdate,
    owner_email: str
) -> TarefasModel | None:
    db_tarefa = get_tarefa(db, tarefa_id, owner_email)
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
    owner_email: str
) -> TarefasModel | None:
    db_tarefa = get_tarefa(db, tarefa_id, owner_email)
    if not db_tarefa:
        return None

    db.delete(db_tarefa)
    db.commit()
    return db_tarefa

def get_tarefas_by_dt_venc(
    db: Session,
    owner_email: str,
    dt_venc: date
) -> List[TarefasModel]:
    return (
        db.query(TarefasModel)
          .filter(
              TarefasModel.owner_email == owner_email,
              TarefasModel.dt_venc == dt_venc
          )
          .all()
    )
