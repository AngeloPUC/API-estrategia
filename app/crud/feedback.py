from sqlalchemy.orm import Session
from typing import List

from app.models.feedback import Feedback as FeedbackModel
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate

def get_feedbacks(
    db: Session,
    owner_email: str,
    skip: int = 0,
    limit: int = 100
) -> List[FeedbackModel]:
    return (
        db.query(FeedbackModel)
          .filter(FeedbackModel.owner_email == owner_email)
          .offset(skip)
          .limit(limit)
          .all()
    )

def get_feedback(
    db: Session,
    feedback_id: int,
    owner_email: str
) -> FeedbackModel | None:
    return (
        db.query(FeedbackModel)
          .filter(
              FeedbackModel.id == feedback_id,
              FeedbackModel.owner_email == owner_email
          )
          .first()
    )

def create_feedback(
    db: Session,
    feedback: FeedbackCreate,
    owner_email: str
) -> FeedbackModel:
    db_feedback = FeedbackModel(**feedback.dict(), owner_email=owner_email)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def update_feedback(
    db: Session,
    feedback_id: int,
    feedback_upd: FeedbackUpdate,
    owner_email: str
) -> FeedbackModel | None:
    db_feedback = get_feedback(db, feedback_id, owner_email)
    if not db_feedback:
        return None

    for key, value in feedback_upd.dict(exclude_unset=True).items():
        setattr(db_feedback, key, value)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def delete_feedback(
    db: Session,
    feedback_id: int,
    owner_email: str
) -> FeedbackModel | None:
    db_feedback = get_feedback(db, feedback_id, owner_email)
    if not db_feedback:
        return None

    db.delete(db_feedback)
    db.commit()
    return db_feedback

def get_feedbacks_by_quem_id(
    db: Session,
    owner_email: str,
    quem_id: int
) -> List[FeedbackModel]:
    return (
        db.query(FeedbackModel)
          .filter(
              FeedbackModel.owner_email == owner_email,
              FeedbackModel.quem_id == quem_id
          )
          .all()
    )
