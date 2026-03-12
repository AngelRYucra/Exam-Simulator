# from pydantic import BaseModel
# from typing import List


# class ExamAnswer(BaseModel):
#     id: int
#     text: str
#     explanation: str | None = None

#     class Config:
#         from_attributes = True


# class ExamQuestion(BaseModel):
#     id: int
#     text: str
#     explanation: str | None = None
#     answers: List[ExamAnswer]

#     class Config:
#         from_attributes = True

# #Frontend sends

# class AnswerSubmission(BaseModel):
#     question_id: int
#     answer_id: int

# class ExamSubmission(BaseModel):
#     answers: List[AnswerSubmission]

# #Backend sends

# class QuestionResult(BaseModel):
#     question_id: int
#     correct: bool
#     correct_answer_id: int | None = None

# class ExamResult(BaseModel):
#     score: int
#     total: int
#     results: List[QuestionResult]

from pydantic import BaseModel
from typing import List, Optional
from app.schemas.question import QuestionLearningResponse

class ExamQuestion(QuestionLearningResponse):
    pass

class AnswerSubmission(BaseModel):
    question_id: int
    answer_id: int

class ExamSubmission(BaseModel):
    answers: List[AnswerSubmission]

class QuestionResult(BaseModel):
    question_id: int
    correct: bool
    correct_answer_id: Optional[int]

class ExamResult(BaseModel):
    score: int
    total: int
    results: List[QuestionResult]