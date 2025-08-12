from sqlalchemy.orm import Session
from typing import List

from app.models.feedback import Feedback as FeedbackModel
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate

def get_feedbacks(db: Session, skip: int = 0, limit: int = 100) -> List[FeedbackModel]:
    return db.query(FeedbackModel).offset(skip).limit(limit).all()

def get_feedback(db: Session, feedback_id: int) -> FeedbackModel | None:
    return db.query(FeedbackModel).filter(FeedbackModel.id == feedback_id).first()

def create_feedback(db: Session, feedback: FeedbackCreate) -> FeedbackModel:
    db_feedback = FeedbackModel(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def update_feedback(db: Session, feedback_id: int, feedback: FeedbackUpdate) -> FeedbackModel | None:
    db_feedback = get_feedback(db, feedback_id)
    if not db_feedback:
        return None
    update_data = feedback.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_feedback, key, value)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def delete_feedback(db: Session, feedback_id: int) -> FeedbackModel | None:
    db_feedback = get_feedback(db, feedback_id)
    if not db_feedback:
        return None
    db.delete(db_feedback)
    db.commit()
    return db_feedback

def get_feedbacks_by_quem_id(db: Session, quem_id: int) -> List[FeedbackModel]:
    return db.query(FeedbackModel).filter(FeedbackModel.quem_id == quem_id).all()
