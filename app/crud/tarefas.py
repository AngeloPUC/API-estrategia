from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.models.tarefas import Tarefas as TarefasModel
from app.schemas.tarefas import TarefasCreate, TarefasUpdate

def get_tarefas(db: Session, skip: int = 0, limit: int = 100) -> List[TarefasModel]:
    return db.query(TarefasModel).offset(skip).limit(limit).all()

def get_tarefa(db: Session, tarefa_id: int) -> TarefasModel | None:
    return db.query(TarefasModel).filter(TarefasModel.id == tarefa_id).first()

def create_tarefa(db: Session, tarefa: TarefasCreate) -> TarefasModel:
    db_tarefa = TarefasModel(**tarefa.dict())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

def update_tarefa(db: Session, tarefa_id: int, tarefa: TarefasUpdate) -> TarefasModel | None:
    db_tarefa = get_tarefa(db, tarefa_id)
    if not db_tarefa:
        return None
    update_data = tarefa.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tarefa, key, value)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

def delete_tarefa(db: Session, tarefa_id: int) -> TarefasModel | None:
    db_tarefa = get_tarefa(db, tarefa_id)
    if not db_tarefa:
        return None
    db.delete(db_tarefa)
    db.commit()
    return db_tarefa

def get_tarefas_by_dt_venc(db: Session, dt_venc: date) -> List[TarefasModel]:
    return db.query(TarefasModel).filter(TarefasModel.dt_venc == dt_venc).all()
