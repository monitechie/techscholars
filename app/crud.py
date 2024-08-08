from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_tests(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Test).offset(skip).limit(limit).all()


def create_test(db: Session, test: schemas.TestCreate):
    db_test = models.Test(title=test.title)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test


def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(text=question.text, test_id=question.test_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def create_answer(db: Session, answer: schemas.AnswerCreate):
    db_answer = models.Answer(
        text=answer.text, question_id=answer.question_id, is_correct=answer.is_correct)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def create_result(db: Session, result: schemas.ResultCreate):
    db_result = models.Result(user_id=result.user_id,
                              test_id=result.test_id, score=result.score)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_results_by_user(db: Session, user_id: int):
    return db.query(models.Result).filter(models.Result.user_id == user_id).all()
