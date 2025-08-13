from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)

@router.post("/", response_model=schemas.feedback.Feedback)
def create_feedback(
    feedback: schemas.feedback.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.feedback.create_feedback(
        db,
        feedback,
        owner_email=owner_email
    )

@router.get("/", response_model=List[schemas.feedback.Feedback])
def read_feedbacks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.feedback.get_feedbacks(
        db,
        owner_email=owner_email,
        skip=skip,
        limit=limit
    )

@router.get("/{feedback_id}", response_model=schemas.feedback.Feedback)
def read_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    db_feedback = crud.feedback.get_feedback(
        db,
        feedback_id,
        owner_email=owner_email
    )
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback não encontrado")
    return db_feedback

@router.put("/{feedback_id}", response_model=schemas.feedback.Feedback)
def update_feedback(
    feedback_id: int,
    feedback: schemas.feedback.FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    updated = crud.feedback.update_feedback(
        db,
        feedback_id,
        feedback,
        owner_email=owner_email
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Feedback não encontrado")
    return updated

@router.delete("/{feedback_id}", response_model=schemas.feedback.Feedback)
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    deleted = crud.feedback.delete_feedback(
        db,
        feedback_id,
        owner_email=owner_email
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Feedback não encontrado")
    return deleted

@router.get("/search/", response_model=List[schemas.feedback.Feedback])
def search_feedbacks(
    quem_id: int = Query(..., description="ID do responsável"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    owner_email = current_user["email"]
    return crud.feedback.get_feedbacks_by_quem_id(
        db,
        owner_email=owner_email,
        quem_id=quem_id
    )
