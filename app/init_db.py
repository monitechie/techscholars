from app.database import Base, engine
from app.models import User, Test, Question, Answer, Result

Base.metadata.create_all(bind=engine)
