# from pydantic import BaseModel
# from typing import Optional, List
# #from app.schemas.answer import AnswerResponse
# from app.schemas.answer import AnswerExamResponse, AnswerLearningResponse


# class QuestionBase(BaseModel):
#     text: str
#     explanation: Optional[str] = None
#     image_url: Optional[str] = None

# class QuestionCreate(QuestionBase):
#     pass

# class QuestionResponse(QuestionBase):
#     id: int

#     class Config:
#         from_attributes = True

# class QuestionWithAnswers(QuestionResponse):
#     answers: list['AnswerExamResponse']

# class QuestionLearningResponse(BaseModel):
#     id: int
#     text: str
#     explanation: Optional[str] = None
#     image_url: Optional[str] = None
#     answers: List[AnswerLearningResponse]

#     class Config:
#         from_attributes = True

from pydantic import BaseModel
from typing import Optional, List
from app.schemas.answer import AnswerResponse

class QuestionLearningResponse(BaseModel):
    id: int
    text: str
    explanation: Optional[str] = None
    image_url: Optional[str] = None
    answers: List[AnswerResponse]

    class Config:
        from_attributes = True

