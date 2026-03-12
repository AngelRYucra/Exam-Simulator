from fastapi import APIRouter
from sqlalchemy.orm import Session, joinedload
from app.database import SessionLocal
from app.models.question import Question
from app.schemas.question import QuestionResponse
from typing import List
from app.schemas.question import QuestionWithAnswers
from fastapi import HTTPException

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

@router.get("/create-test")
def get_questions():
    db: Session = SessionLocal()

    question = Question(text="What does a red light mean?")
    db.add(question)
    db.commit()
    db.refresh(question)

    db.close()

    return {"message": "Test question created", "question_id": question.id}

@router.get("/", response_model=List[QuestionResponse])
def get_questions():
    db: Session = SessionLocal()
    questions = db.query(Question).all()
    db.close()

    return questions

@router.get("/{question_id}", response_model=QuestionWithAnswers)
def get_question_by_id(question_id: int):
    db: Session = SessionLocal()

    question = (
        db.query(Question)
        .options(joinedload(Question.answers))
        .filter(Question.id == question_id)
        .first()
    )

    db.close()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question
