from pydantic import BaseModel
from typing import List


class SubmittedAnswer(BaseModel):
    question_id: int
    answer_id: int


class ExamSubmission(BaseModel):
    answers: List[SubmittedAnswer]


class QuestionResult(BaseModel):
    question_id: int
    correct: bool
    correct_answer: str
    explanation: str


class ExamResult(BaseModel):
    score: int
    total: int
    results: List[QuestionResult]
