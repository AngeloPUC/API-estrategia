# app/routers/tarefas.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app import crud, schemas
from app.database import get_db
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/tarefas",
    tags=["Tarefas"],
)

@router.post("/", response_model=schemas.tarefas.Tarefas)
def create_tarefa(
    tarefa: schemas.tarefas.TarefasCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return crud.tarefas.create_tarefa(
        db,
        tarefa,
        dono=current_user["email"]
    )

@router.get("/", response_model=List[schemas.tarefas.Tarefas])
def read_tarefas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return crud.tarefas.get_tarefas(
        db,
        dono=current_user["email"],
        skip=skip,
        limit=limit
    )

@router.get("/{tarefa_id}", response_model=schemas.tarefas.Tarefas)
def read_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_tarefa = crud.tarefas.get_tarefa(
        db,
        tarefa_id,
        dono=current_user["email"]
    )
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

@router.put("/{tarefa_id}", response_model=schemas.tarefas.Tarefas)
def update_tarefa(
    tarefa_id: int,
    tarefa: schemas.tarefas.TarefasUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    updated = crud.tarefas.update_tarefa(
        db,
        tarefa_id,
        tarefa,
        dono=current_user["email"]
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return updated

@router.delete("/{tarefa_id}", response_model=schemas.tarefas.Tarefas)
def delete_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    deleted = crud.tarefas.delete_tarefa(
        db,
        tarefa_id,
        dono=current_user["email"]
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return deleted

@router.get("/search/", response_model=List[schemas.tarefas.Tarefas])
def search_tarefas(
    dt_venc: date = Query(..., description="Data de vencimento"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return crud.tarefas.get_tarefas_by_dt_venc(
        db,
        dono=current_user["email"],
        dt_venc=dt_venc
    )
