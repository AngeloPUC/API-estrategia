# app/crud/esteira.py
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.esteira import Esteira as EsteiraModel
from app.schemas.esteira import EsteiraCreate, EsteiraUpdate

def get_esteiras(
    db: Session,
    owner_email: str,
    skip: int = 0,
    limit: int = 100
) -> List[EsteiraModel]:
    return (
        db.query(EsteiraModel)
          .filter(EsteiraModel.owner_email == owner_email)
          .offset(skip)
          .limit(limit)
          .all()
    )

def get_esteira(
    db: Session,
    esteira_id: int,
    owner_email: str
) -> Optional[EsteiraModel]:
    return (
        db.query(EsteiraModel)
          .filter(
              EsteiraModel.id == esteira_id,
              EsteiraModel.owner_email == owner_email
          )
          .first()
    )

def create_esteira(
    db: Session,
    esteira: EsteiraCreate,
    owner_email: str
) -> EsteiraModel:
    db_row = EsteiraModel(**esteira.dict(), owner_email=owner_email)
    db.add(db_row)
    db.commit()
    db.refresh(db_row)
    return db_row

def update_esteira(
    db: Session,
    esteira_id: int,
    esteira_upd: EsteiraUpdate,
    owner_email: str
) -> Optional[EsteiraModel]:
    db_row = get_esteira(db, esteira_id, owner_email)
    if not db_row:
        return None

    for key, value in esteira_upd.dict(exclude_unset=True).items():
        setattr(db_row, key, value)
    db.commit()
    db.refresh(db_row)
    return db_row

def delete_esteira(
    db: Session,
    esteira_id: int,
    owner_email: str
) -> Optional[EsteiraModel]:
    db_row = get_esteira(db, esteira_id, owner_email)
    if not db_row:
        return None

    db.delete(db_row)
    db.commit()
    return db_row

def get_esteiras_by_cnpjcpf(
    db: Session,
    owner_email: str,
    cnpjcpf: str
) -> List[EsteiraModel]:
    return (
        db.query(EsteiraModel)
          .filter(
              EsteiraModel.owner_email == owner_email,
              EsteiraModel.cnpjcpf == cnpjcpf
          )
          .all()
    )

def get_esteiras_by_data(
    db: Session,
    owner_email: str,
    data
) -> List[EsteiraModel]:
    return (
        db.query(EsteiraModel)
          .filter(
              EsteiraModel.owner_email == owner_email,
              EsteiraModel.data == data
          )
          .all()
    )
