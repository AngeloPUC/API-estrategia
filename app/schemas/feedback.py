from pydantic import BaseModel
from typing import Optional

class FeedbackBase(BaseModel):
    titulo: str
    base: str
    descricao: Optional[str] = None
    resultado: int
    quem_id: int
    feedback: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    titulo: Optional[str] = None
    base: Optional[str] = None
    descricao: Optional[str] = None
    resultado: Optional[int] = None
    quem_id: Optional[int] = None
    feedback: Optional[str] = None

class Feedback(FeedbackBase):
    id: int

    class Config:
        from_attributes = True
