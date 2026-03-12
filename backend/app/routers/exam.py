
from fastapi import APIRouter, HTTPException
from app.schemas.exam import ExamQuestion, ExamSubmission, ExamResult
from app.schemas.question import QuestionLearningResponse
from app.services.exam_service import exam_service

router = APIRouter(
    prefix="/exam",
    tags=["Exam"]
)

number_of_questions = 40

@router.get("/", response_model=list[ExamQuestion])
def get_exam():
    """Devuelve un examen de 10 preguntas aleatorias."""
    return exam_service.get_random_questions(number_of_questions)

@router.get("/all", response_model=list[ExamQuestion])
def get_exam_all():
    """Devuelve todo el banco de preguntas."""
    return exam_service.get_all_questions()

@router.get("/learn", response_model=QuestionLearningResponse)
def get_learning_question():
    """Devuelve una pregunta aleatoria para el modo aprendizaje."""
    return exam_service.obtener_pregunta_aleatoria()

@router.get("/visual-learn", response_model=QuestionLearningResponse)
def get_visual_learning_question():
    """Devuelve una pregunta de señales para el modo visual."""
    return exam_service.obtener_pregunta_visual()

@router.get("/{id:int}")
def get_exam_id(id: int):
    """Busca una pregunta específica por su ID."""
    question = exam_service.get_question_by_id(id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.post("/submit", response_model=ExamResult)
def submit_exam(submission: ExamSubmission):
    """Recibe las respuestas del usuario y califica el simulacro."""
    return exam_service.evaluate_exam(submission)


# from app.schemas.question import QuestionLearningResponse
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session, joinedload
# from sqlalchemy.sql.expression import func
# from app.database import SessionLocal
# from app.models.question import Question
# from app.schemas.exam import ExamQuestion
# from app.database import get_db
# from app.models.answer import Answer
# from app.schemas.exam import ExamSubmission, ExamResult, QuestionResult
# from app.schemas.answer import AnswerExamResponse, AnswerLearningResponse

# router = APIRouter(
#     prefix="/exam",
#     tags=["Exam"]
# )

# number_of_questions = 10

# @router.get("/", response_model=list[ExamQuestion])
# def get_exam(db: Session = Depends(get_db)):

#     questions = (
#         db.query(Question)
#         .options(joinedload(Question.answers))
#         .order_by(func.random())
#         .limit(number_of_questions)
#         .all()
#     )

#     return questions

# @router.get("/all", response_model=list[ExamQuestion])
# def get_exam_all(db: Session = Depends(get_db)):

#     questions = (
#         db.query(Question)
#         .options(joinedload(Question.answers))
#         .all()
#     )

#     return questions

# @router.get("/learn", response_model=QuestionLearningResponse)
# def get_learning_question(db: Session = Depends(get_db)):

#     question = (
#         db.query(Question)
#         .options(joinedload(Question.answers))
#         .order_by(func.random())
#         .first()
#     )

#     # If there are no questions in the database, return a 404 error

#     return question

# @router.get("/visual-learn", response_model=QuestionLearningResponse)
# def get_visual_learning_question(db: Session = Depends(get_db)):

#     question = (
#         db.query(Question)
#         .options(joinedload(Question.answers))
#         .filter(Question.image_url != None)
#         .order_by(func.random())
#         .first()
#     )

#     # If there are no questions in the database, return a 404 error

#     return question

# @router.get("/{id:int}")
# def get_exam_id(id: int, db: Session = Depends(get_db)):

#     question = (
#         db.query(Question)
#         .options(joinedload(Question.answers))
#         .filter(Question.id==id)
#         .first()
#     )

#     if not question:
#         raise HTTPException(status_code=404, detail="Question not found")

#     return question


# @router.post("/submit", response_model=ExamResult)
# def submit_exam(
#     submission: ExamSubmission,
#     db: Session = Depends(get_db)
# ):
#     score = 0
#     results = []

#     for item in submission.answers:
#         correct_answer = (
#             db.query(Answer)
#             .filter(
#                 Answer.question_id == item.question_id,
#                 Answer.is_correct == True
#             )
#             .first()
#         )

#         if not correct_answer:
#             continue

#         is_correct = correct_answer.id == item.answer_id

#         if is_correct:
#             score += 1

#         results.append(
#             QuestionResult(
#                 question_id=item.question_id,
#                 correct=is_correct,
#                 correct_answer_id=None if is_correct else correct_answer.id
#             )
#         )

#     return ExamResult(
#         score=score,
#         total=len(submission.answers),
#         results=results
#     )

