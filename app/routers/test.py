from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Answer, Test, Question, User, UserTest
from app.dependencies import admin_required, get_current_user
from pydantic import BaseModel

from app.schemas import TestBase, TestSubmission, TestUpdate, UserTestResult

router = APIRouter()


class QuestionCreate(BaseModel):
    text: str
    test_id: int


class TestCreate(BaseModel):
    title: str


class AnswerCreate(BaseModel):
    text: str
    question_id: int
# To create test


@router.post("/tests")
def create_test(title: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")
    db_test = Test(title=title)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return {"msg": "Test created successfully", "test_id": db_test.id}


@router.post("/questions")
def add_question(question: QuestionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")
    # Check if the test exists
    db_test = db.query(Test).filter(Test.id == question.test_id).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")

    # Add the new question
    db_question = Question(text=question.text, test_id=question.test_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return {"msg": "Question added successfully"}


@router.post("/answer")
def add_answer(answer: AnswerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")
    db_answer = Answer(text=answer.text, question_id=answer.question_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return {"msg": "Answer added successfully"}


@router.get("/", response_model=List[TestBase])
def get_tests(db: Session = Depends(get_db)):
    return db.query(Test).all()
# Update test


@router.put("/{test_id}", response_model=TestBase)
def update_test(test_id: int, test: TestUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")
    if test.title is not None:
        db_test.title = test.title
    db.commit()
    db.refresh(db_test)
    return db_test
# Delete test


@router.delete("/{test_id}", response_model=TestBase)
def delete_test(test_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")
    db.delete(db_test)
    db.commit()
    return db_test


@router.post("/submit", response_model=UserTestResult)
def submit_test(submission: TestSubmission, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    test = db.query(Test).filter(Test.id == submission.test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    score = len(submission.answers)

    user_test = UserTest(user_id=current_user.id,
                         test_id=submission.test_id, score=score)
    db.add(user_test)
    db.commit()
    db.refresh(user_test)

    return user_test


@router.get("/results", response_model=List[UserTestResult])
def get_my_results(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(UserTest).filter(UserTest.user_id == current_user.id).all()
