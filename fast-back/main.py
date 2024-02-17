from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

class LoginBase(BaseModel):
    masonid: str
    password: str

class LoginModel(LoginBase):

    class Config:
        orm_mode = True

# close database when request is complete
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# automate table creation
db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)


@app.post("/logins/", response_model=LoginModel)
async def create_login(login: LoginBase, db: db_dependency):
    db_login = models.Login(**login.model_dump())  # Change Transaction to Login
    db.add(db_login)
    db.commit()
    db.refresh(db_login)
    return db_login
