from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.models.acoes import Acoes as AcoesModel
from app.schemas.acoes import AcoesCreate, AcoesUpdate

def get_acoes(db: Session, skip: int = 0, limit: int = 100) -> List[AcoesModel]:
    return db.query(AcoesModel).offset(skip).limit(limit).all()

def get_acao(db: Session, acao_id: int) -> AcoesModel | None:
    return db.query(AcoesModel).filter(AcoesModel.id == acao_id).first()

def create_acao(db: Session, acao: AcoesCreate) -> AcoesModel:
    db_acao = AcoesModel(**acao.dict())
    db.add(db_acao)
    db.commit()
    db.refresh(db_acao)
    return db_acao

def update_acao(db: Session, acao_id: int, acao: AcoesUpdate) -> AcoesModel | None:
    db_acao = get_acao(db, acao_id)
    if not db_acao:
        return None
    update_data = acao.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_acao, key, value)
    db.commit()
    db.refresh(db_acao)
    return db_acao

def delete_acao(db: Session, acao_id: int) -> AcoesModel | None:
    db_acao = get_acao(db, acao_id)
    if not db_acao:
        return None
    db.delete(db_acao)
    db.commit()
    return db_acao

def get_acoes_by_quem_id_and_dt_venc(
    db: Session, quem_id: int, dt_venc: date
) -> List[AcoesModel]:
    return (
        db.query(AcoesModel)
        .filter(AcoesModel.quem_id == quem_id, AcoesModel.dt_venc == dt_venc)
        .all()
    )
