# from pydantic import BaseModel
# from typing import Optional

# class AnswerBase(BaseModel):
#     text: str
#     explanation: Optional[str] = None

# class AnswerCreate(AnswerBase):
#     question_id: int

# class AnswerExamResponse(AnswerBase):
#     id: int
#     question_id: int

#     class Config:
#         from_attributes = True

# class AnswerLearningResponse(AnswerBase):
#     id: int
#     question_id: int
#     is_correct: bool

#     class Config:
#         from_attributes = True

from pydantic import BaseModel
from typing import Optional

class AnswerResponse(BaseModel):
    id: int
    text: str
    is_correct: Optional[bool] = None
    explanation: Optional[str] = None

    class Config:
        from_attributes = True