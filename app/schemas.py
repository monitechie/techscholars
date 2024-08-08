from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class TestBase(BaseModel):
    title: str

    class Config:
        orm_mode = True


class TestCreate(TestBase):
    pass


class TestUpdate(BaseModel):
    title: Optional[str] = None


class Test(TestBase):
    id: int

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    text: str

    class Config:
        orm_mode = True


class QuestionCreate(QuestionBase):
    test_id: int


class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True


class AnswerBase(BaseModel):
    text: str
    is_correct: Optional[int] = 0


class AnswerCreate(AnswerBase):
    question_id: int


class Answer(AnswerBase):
    id: int

    class Config:
        orm_mode = True


class AnswerSubmission(BaseModel):
    question_id: int
    answer_id: int


class TestSubmission(BaseModel):
    test_id: int
    answers: List[AnswerCreate]


class UserTestResult(BaseModel):
    test_id: int
    score: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
